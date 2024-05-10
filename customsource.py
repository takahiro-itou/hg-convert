import hgext.convert.convcmd

from hgext.convert.hg import mercurial_source as basesource
#from hgext.convert.subversion import svn_source as basesource # to use subversion as source

class customsource(basesource):

    def getchanges(self, version, full):
        # returns (filename, rev) list and target, source dictionary
        # files not included in the list is just ignored
        files, copies, cleanp2 = super(customsource, self).getchanges(version, full)
        return files, copies, cleanp2

    def getcommit(self, rev):
        # returns meta data for changeset rev
        c = super(customsource, self).getcommit(rev)
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

    def getfile(self, name, rev):
        # returns file content and flags for named file at revision
        data, flags = super(customsource, self).getfile(name, rev)
        if data is None or b'nuclear launch code' in data:
            # the change is that the file is removed
            return None, None
            # raise IOError # for Mercurial < 3.2

        # use case: modify file data
        if rev == b'f8b4ca9f6ffeb6b288be4c44e4d55458f867cd7c' and name == b'foo':
            data = b'yo\nyo\n'

        # use case: tagmap
        if name == b'.hgtags':
            data = b''.join(line[:41] + tagmap(line[41:]) + b'\n'
                           for line in data.splitlines())

        return data, flags

    # use case: tagmap
    def gettags(self):
        return dict((tagmap(tag), node)
                    for tag, node in super(customsource, self).gettags().items())

# use case: tagmap
def tagmap(tag):
    return tag.replace(b'some', b'other')

hgext.convert.convcmd.source_converters.append((b'customsource', customsource, b'branchsort'))
