from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from ordinance.models import Ordinance
from councilmeeting.models import CouncilMeeting
from school.models import CanteenMenu


class OrdinanceViewSet(SnippetViewSet):
    model = Ordinance
    icon = "warning"
    menu_label = "Arrêtés"
    menu_name = "ordinance"
    list_display = ["date", "author", "get_type_display"]
    list_per_page = 20
    list_filter = ["type", "author"]


class CouncilMeetingViewSet(SnippetViewSet):
    model = CouncilMeeting
    icon = "doc-full"
    menu_label = "Réunions du conseil"
    menu_name = "council_meeting"
    list_display = ["date", "author"]
    list_per_page = 20


class OrdinanceCouncilViewSetGroup(SnippetViewSetGroup):
    items = (OrdinanceViewSet, CouncilMeetingViewSet)
    menu_icon = "circle-plus"
    menu_label = "Arrêtés / Comptes-rendus"
    menu_name = "ordinance_council"


class CanteenMenuPageViewSet(SnippetViewSet):
    model = CanteenMenu
    icon = "group"
    menu_label = "Menus Cantine"
    menu_name = "canteen_menu_page"
    list_display = ["date", "author"]
    list_per_page = 20


class CanteenMenuPageViewSetGroup(SnippetViewSetGroup):
    items = (CanteenMenuPageViewSet,)
    menu_icon = "group"
    menu_label = "Menus Cantine"
    menu_name = "canteen_menu_page_group"


register_snippet(OrdinanceCouncilViewSetGroup)
register_snippet(CanteenMenuPageViewSetGroup)
