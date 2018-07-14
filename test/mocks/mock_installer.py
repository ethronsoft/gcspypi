class MockInstaller(object): # pragma: no cover

    def __init__(self):
        self.installed = {}
        self.uninstalled = {}

    def install(self, resource, flags=[]):
        self.installed[resource] = self.installed.get("resource", 0) + 1
    
    def uninstall(self, pkg):
        self.uninstalled[pkg.full_name] = self.uninstalled.get(pkg.full_name, 0) + 1