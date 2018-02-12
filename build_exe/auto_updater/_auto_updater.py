import os
from mmpe.ui.text_ui import TextUI
from mmpe.io.html import HTML
import shutil
from mmpe.build_exe.version_utils import extract_version, version_str

class AutoUpdater(HTML):
    def __init__(self, url, folder, app_name, keep=2, ui = TextUI()):
        self.url = url
        self.app_name = app_name
        self.folder = self._get_app_folder(folder)
        self.keep = keep
        self._versions = None
        self.ui = ui
        
    @property
    def versions(self):
        if self._versions is None:
            self.get_version_info()
        return self._versions
        
    @property
    def info_dict(self):
        if self.versions is None:
            self.get_version_info()
        return self._info_dict
        
    def info(self, version):
        return self.info_dict[str(version)]

    def get_version_info(self):
        html = self.read(self.url)
        
        def to_dict(info):
            version, date, exe_name,zip_name,news = [tag.replace("</TD>","").strip() for tag in info.split("<TD>")[1:]]
            return {'version':tuple(int(v) for v in version.replace("Version","").split(".")),
                    "date": date,
                    "exe": exe_name.split('"')[1],
                    "zip": zip_name.split('"')[1],
                    "news": [l.split("</li>")[0].strip() for l in news.split("<li>")[1:]]}
        info_lst = [to_dict(version) for version in html.split("<TR>")[2:]]
        versions = [info["version"] for info in info_lst]
        self._info_dict = {str(version):info for version,info in zip(versions, info_lst)}
        self._versions = sorted(versions, reverse=True)
        return self._versions, self._info_dict
    
    def update(self, version):
        filename = self._download_zip(version)
        tmp_unzip = os.path.join(self.folder, "tmp_unzip/")
        import zipfile
        def unzip():
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(tmp_unzip)
        self.ui.exec_long_task("Unzipping downloaded version", False, unzip)
        os.remove(filename)
        unzip_app_folder = os.path.join(tmp_unzip, self.app_name + "/")
        app_folder = self.folder
        for f in os.listdir(unzip_app_folder):
            if os.path.exists(os.path.join(self.folder, f)):
                if os.path.isfile(os.path.join(self.folder, f)):
                    os.remove(os.path.join(self.folder, f))
                elif os.path.isdir(os.path.join(self.folder, f)):
                    shutil.rmtree(os.path.join(self.folder, f))
            shutil.move(os.path.join(unzip_app_folder, f), self.folder)
        shutil.rmtree(tmp_unzip)
        self.remove_old_versions()
                
    def remove_old_versions(self):
        version_dict = self.get_local_versions()
        if len(version_dict)>self.keep:
            for v in sorted(version_dict.keys())[:-2]:
                shutil.rmtree(os.path.join(self.folder, version_dict[v]))
                
        
        
    def _download_zip(self, version):
        zip_name = self.info(version)['zip']
        source = "/".join(self.url.split('/')[:-1]) + "/"+zip_name
        filename = os.path.join(self.folder, zip_name)
        return self.download(source, filename)
    
    def _get_app_folder(self, folder):
        if not os.path.split(os.path.abspath(folder))[1].startswith(self.app_name):
            folder = os.path.join(folder, self.app_name+"/")
        elif os.path.split(os.path.abspath(os.path.join(folder, "../")))[1]==self.app_name:
            folder = os.path.abspath(os.path.join(folder + "../"))
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return folder
            
                        
        
    
    def get_local_versions(self):
        if os.path.split(os.path.abspath(self.folder))[1]==self.app_name:
            versions, version_dict = [], {}
            for f in os.listdir(self.folder):
                v = extract_version(f)
                if v:
                    versions.append(v)
                    version_dict[version_str(v)] = f
            return versions, version_dict
        raise FileNotFoundError("Folder '%s' not found in ''"%(self.app_name, self.folder))
    
    def check_for_updates(self):
        current_version = sorted(self.get_local_versions()[0])[-1]
        newest_version = sorted(self.versions)[-1]
        if newest_version > current_version:
            
            msg = "Current version: %s\nAvailable version: %s\n\n" % (version_str(current_version), version_str(newest_version))
            if len(self.info(newest_version)['news']) and self.info(newest_version)['news'][0][0]=="!":
                msg += "%s\n\n"%self.info(newest_version)['news'][0][1:]
            msg += "Do you want to download and install the update?"
            
            if self.ui.get_confirmation("Update", msg):
                self.update(newest_version)
            