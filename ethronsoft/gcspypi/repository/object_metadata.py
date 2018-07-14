class ObjectMetadata(object):
    """ObjectMetadata represents the metadata associated with a repository Object
    """

    def __init__(self, mime, md5_hash, time_created):
        """ObjectMetadata constructor
        
        Arguments:
            mime {str} -- MIME type of object
            md5_hash {str} -- Hash representing the object. Can be used to determine content equality
            time_created {datetime} -- Timestamp for the object creation
        """

        self.mime = mime
        self.md5 = md5_hash
        self.time_created = time_created
 