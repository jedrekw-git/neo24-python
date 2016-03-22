from pages.page import Page

class BasePage(Page):

    _base_url = "http://www.neo24.pl/"

    @property
    def header(self):
        from pages.regions.header_region import HeaderRegion
        return HeaderRegion(self.get_driver())
