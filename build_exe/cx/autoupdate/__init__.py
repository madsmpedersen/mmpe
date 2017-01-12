import os
import sys
from mmpe.ui import UI

def autoupdate(update_page, ui, name=""):
    from esky import Esky
    assert isinstance(ui, UI)

    if hasattr(sys, "frozen"):
        esky = Esky(sys.executable, update_page)
    else:
        #return
        esky = Esky(os.path.dirname(__file__), update_page)
        esky.name = name

    got_root = False
    cleaned = False
    ui.start_blocking_task("Searching for updates")
    try:
        version = esky.find_update()
    except Exception as e:
        sys.stderr.write("Could not find updates: \n" + str(e))
        version = None
    finally:
        ui.end_blocking_task()
    if version is not None:
        msg = "Current version: %s\nAvailable version: %s\n\nDo you want to download and install the update?" % (esky.version, version)
        if ui.get_confirmation("New version available", msg):
            def callback(kwargs):
                if kwargs['status'] == "downloading":
                    current = kwargs['received']
                    maximum = kwargs['size']
                    ui._callback(current, maximum)
                else:
                    title = kwargs['status']
                    ui.start_blocking_task(title[0].upper() + title[1:])

            try:
                loc = ui.exec_long_task_with_callback("Downloading new version", True, esky.fetch_version, version, callback)
            except Exception as e:

                e.args = ("Downloading new version failed\n",)
                ui.show_error(e)
                return
            finally:
                ui.end_blocking_task()

            if os.path.isdir(loc):
                ui.start_blocking_task("Installing")
                esky.install_version(version)
                ui.end_blocking_task()

                try:
                    ui.start_blocking_task("Uninstalling previous version")
                    esky.uninstall_version(esky.version)
                except Exception:
                    pass
                finally:
                    ui.end_blocking_task()
                try:
                    esky.get_root()
                except Exception as e:
                    pass
                else:
                    got_root = True
                    callback({"status":"cleaning up"})

                    cleaned = esky.cleanup()
                #  Drop root privileges as soon as possible.
                if not cleaned and esky.needs_cleanup():
                    try:
                        esky.cleanup_at_exit()
                    except:
                        pass

                if got_root:
                    esky.drop_root()
                ui.end_blocking_task()
                ui.show_message("Update complete\n\nPlease restart %s" % esky.name, "Update complete")
                #sys.exit(0)
