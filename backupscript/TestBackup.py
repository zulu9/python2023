import unittest
import subprocess
from Backup import Backup
from os import path, remove, getcwd

pwd = getcwd()

class TestBackup(unittest.TestCase):

    def setUp(this):
        this.backup = Backup(None, "test")
        this.backup.log_file_path = f"{pwd}/log.txt"
        this.backup.rsync_log_file_path = f"{pwd}/rsync-log.txt"
        this.backup.backup_lockfile_path = f"{pwd}/backup-lockfile.lock"
        this.backup.veeam_lockfile_dir = f"{pwd}/veeam-lockfile.lock"
        this.backup.backup_source = f"{pwd}"

    def testCanFindExistingUUID(this):
        this.backup.uuids_mailaddresses_list = [subprocess.getoutput("sudo blkid -s UUID -o value").split("\n")[0]]
        this.assertEqual(this.backup.checkFilesystem(), 0)

    def testRaisesExceptionIfCanNotFindExistingUUID(this):
        this.backup.uuids_mailaddresses_list = [subprocess.getoutput("sudo blkid -s UUID -o value").split("\n")[0] + "test"]
        this.assertRaises(ValueError, this.backup.checkFilesystem)

    def testContinueWhenNoVeeamLockfileIsDetected(this):
        this.assertEqual(this.backup.checkVeeamBackup(), 0)

    def testRaisesExceptionIfVeeamLockfileStillExistsAfterTimeout(this):
        open(f"{this.backup.veeam_lockfile_dir}", "w").close()
        this.backup.wait_for_veeam_minutes = -1
        this.assertRaises(ValueError, this.backup.checkVeeamBackup)
        remove(this.backup.veeam_lockfile_dir)

    def testRaisesExceptionIfMountNotPossible(this):
        this.backup.uuid = [subprocess.getoutput("sudo blkid -s UUID -o value").split("\n")[0] + "test"]
        this.assertRaises(ValueError, this.backup.mountHDD)

    def testCanCreateLockfile(this):
        this.assertEqual(this.backup.createLockfile(), 0)
        remove(this.backup.backup_lockfile_path)

    def testWarnsIfLockfileExistsWithNoLock(this):
        file = open(f"{this.backup.backup_lockfile_path}", "w"); file.close()
        this.assertWarns(Warning, this.backup.createLockfile)
        remove(this.backup.backup_lockfile_path)

    def testRaisesExceptionIfLockfileExistsWithLock(this):
        file = open(f"{this.backup.backup_lockfile_path}", "w"); file.write("locked"); file.close()
        this.assertRaises(ValueError, this.backup.createLockfile)
        remove(this.backup.backup_lockfile_path)

    def testCanCopyFiles(this):
        subprocess.run(f"sudo mkdir {pwd}/A", shell=True)
        subprocess.run(f"sudo mkdir {pwd}/B", shell=True)
        subprocess.run(f"sudo fallocate -l 1K {pwd}/A/file.img", shell=True)
        this.backup.backup_source = f"{pwd}/A"
        this.backup.backup_destination = f"{pwd}/B"

        this.assertEqual(this.backup.startCopy(), 0)
        this.assertEqual(path.getsize(f"{pwd}/A/file.img"), path.getsize(f"{pwd}/B/A/file.img"))

        subprocess.run(f"sudo rm -R {pwd}/A", shell=True)
        subprocess.run(f"sudo rm -R {pwd}/B", shell=True)
        subprocess.run(f"sudo rm {this.backup.rsync_log_file_path}", shell=True)

    def testCanDeleteLockfile(this):
        open(f"{this.backup.backup_lockfile_path}", "w").close()
        this.assertEqual(this.backup.deleteLockfile(), 0)

    def testRaisesExceptionTryDeleteNotExistingLockfile(this):
        this.assertWarns(Warning, this.backup.deleteLockfile)

if __name__ == '__main__':
    unittest.main()