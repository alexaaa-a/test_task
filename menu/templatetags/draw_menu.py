from django import template
from django.http import HttpRequest
from ..models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('draw_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    """Отображает древовидное меню с учетом активного пункта"""
    request = context.get('request')

    if not isinstance(request, HttpRequest):
        return {'menu_tree': []}

    try:
        menu_items = MenuItem.objects.filter(
            menu__name=menu_name
        ).select_related('parent')

        menu_tree = build_menu_tree(menu_items)

        current_path = request.path
        active_items = find_active_items(menu_items, current_path)

        mark_expanded_branches(menu_tree, active_items)

        return {
            'menu_tree': menu_tree,
            'menu_name': menu_name
        }

    except Menu.DoesNotExist:
        return {'menu_tree': []}


def build_menu_tree(items):
    """Строит иерархическую структуру меню"""
    item_dict = {item.id: {'item': item, 'children': []} for item in items}
    root_items = []

    for item in items:
        if item.parent_id and item.parent_id in item_dict:
            item_dict[item.parent_id]['children'].append(item_dict[item.id])
        else:
            root_items.append(item_dict[item.id])

    return root_items


def find_active_items(items, current_path: str):
    """Находит активные пункты меню по текущему URL"""
    active_ids = set()

    for item in items:
        if item.url and item.url == current_path:
            parent = item
            while parent:
                active_ids.add(parent.id)
                parent = parent.parent
            break

    return active_ids


def mark_expanded_branches(tree_nodes, active_ids):
    """Рекурсивно помечает узлы для раскрытия"""
    for node in tree_nodes:
        node['is_expanded'] = node['item'].id in active_ids
        node['is_active'] = node['item'].id in active_ids

        if node['children']:
            mark_expanded_branches(node['children'], active_ids)
            if any(child['is_active'] for child in node['children']):
                node['is_expanded'] = True