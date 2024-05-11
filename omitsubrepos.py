import hgext.convert.convcmd

from hgext.convert.hg import mercurial_source as basesource

import logging
import sys

logging.basicConfig(
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    style='%',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class OmitSubRepos(basesource):

    def getchanges(self, version, full):
        # returns (filename, rev) list and target, source dictionary
        # files not included in the list is just ignored
        files, copies, cleanp2 = super(OmitSubRepos, self).getchanges(version, full)
        logger.debug("files = {}".format(files,))
        files_new = []
        files_append = files_new.append
        for x in files:
            if x[0] == b'.hgsub':
                logger.info("Skipping {}".format(x,))
            elif x[0] == b'.hgtags':
                logger.info("Skipping {}".format(x,))
            else:
                files_append(x)
            # End If
        # Next (x)
        return files_new, copies, cleanp2

    def getcommit(self, rev):
        # returns meta data for changeset rev
        c = super(OmitSubRepos, self).getcommit(rev)
        logger.debug("commit = {}".format(c.__dict__,))
        return c
    # End Def (getcommit)

# End Class (OmitSubRepos)


logger.debug(sys.version)

hgext.convert.convcmd.source_converters.append(
    (b'hg-omit-subrepos', OmitSubRepos, b'datesort')
)
