import hgext.convert.convcmd

from hgext.convert.hg import mercurial_source as basesource
#from hgext.convert.subversion import svn_source as basesource # to use subversion as source

import logging
import sys

logging.basicConfig(
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    style='%',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class customsource(basesource):

    def getchanges(self, version, full):
        # returns (filename, rev) list and target, source dictionary
        # files not included in the list is just ignored
        files, copies, cleanp2 = super(customsource, self).getchanges(version, full)
        logger.debug("files = {}".format(files,))
        files_new = [ x for x in files if x[0] != b'.hgsub' ]
        return files_new, copies, cleanp2

    def getcommit(self, rev):
        # returns meta data for changeset rev
        c = super(customsource, self).getcommit(rev)
        logger.debug("commit = {}".format(c.__dict__,))
        c.extra = c.extra.copy()

        # use case: authormapsuffix
        c.author = c.author.split(b'@', 1)[0] + b'@FreeBSD.org'

        # use case: closemap
        if rev in b'''
            d643f67092ff123f6a192d52f12e7d123dae229f
            9117c6561b0bd7792fa13b50d28239d51b78e51f
            ''':
            c.extra[b'close'] = b'1'

        # use case: branchmap
        if c.branch == b'default':
            c.branch = b'trunk'

        # use case: modify descriptions
        c.desc = c.desc.title()

        # use case: modify time
        c.date = b'1971-02-03 04:05:06 +0000'

        return c

# End Class (customsource)


logger.debug(sys.version)

hgext.convert.convcmd.source_converters.append((b'customsource', customsource, b'branchsort'))
