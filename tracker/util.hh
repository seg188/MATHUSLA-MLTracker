#include <iostream>
#include <dirent.h>

#ifndef UTIL_HH
#define UTIL_HH

namespace io {

void ProcessDirectory(std::string directory, std::string current_path, std::vector<TString>* files, bool done = 0)
{
   std::string path_to_dir = current_path + directory;
   std::string new_path = path_to_dir + '/';
   std::cout << "beep" << std::endl;
   auto dir = opendir(path_to_dir.c_str());
   if (dir == NULL)
   {
      std::cout << "Could not open directory: " << directory.c_str() << std::endl;
      return;
   }

   auto entity = readdir(dir);
   while (entity != NULL)
   {
      
      if(entity->d_type == DT_DIR) 
      {
         bool do_process = true;

            if(entity->d_name[0] == '.') 
            {
               do_process = false;
            }

            if (do_process)
            {
               ProcessDirectory(std::string(entity->d_name), new_path, files, 0);
            }
        }

        if(entity->d_type == DT_REG)
        {
          //std::cout << TString(entity->d_name) << std::endl;
          TString file_name = TString(entity->d_name);
          if (file_name.EndsWith(".root")) files->push_back(TString(new_path) + TString(entity->d_name));
          //ProcessFile(std::string(entity->d_name), new_path);
        }

      entity = readdir(dir);
   }
   
   closedir(dir);

}


}; //namespace io

#endif