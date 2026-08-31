# Embedded file name: scripts/client/CorruptedPacks.py
import os
__author__ = 'muzhig'

class CorruptedPacks:

    def onCorruptedPacks(self, pack_names):
        if len(pack_names):
            with open('corrupted', 'w') as f:
                f.write('\n'.join(pack_names))
        elif os.path.isfile('corrupted'):
            os.remove('corrupted')

    def onCorruptedPack(self, pack_name):
        if pack_name:
            corrupted = self.getCorruptedPacks()
            if pack_name not in corrupted:
                corrupted.append(pack_name)
                with open('corrupted', 'w') as f:
                    f.write('\n'.join(corrupted))

    def onValidPack(self, pack_name):
        if pack_name:
            corrupted = self.getCorruptedPacks()
            if pack_name in corrupted:
                corrupted.remove(pack_name)
                with open('corrupted', 'w') as f:
                    f.write('\n'.join(corrupted))

    @staticmethod
    def getCorruptedPacks():
        if os.path.isfile('corrupted'):
            with open('corrupted', 'r') as f:
                pack_names = list(filter(None, (line.strip() for line in f)))
            return pack_names
        else:
            return []
            return