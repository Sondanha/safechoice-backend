class ExternalScenarioCollector:
    """
    Placeholder for automated scenario / document ingestion.
    Not used in runtime service.
    """

    def fetch(self):
        raise NotImplementedError

    def normalize(self, raw):
        raise NotImplementedError

    def store(self, data):
        raise NotImplementedError
