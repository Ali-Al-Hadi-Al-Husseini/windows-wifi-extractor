import subprocess

def main():
    # using netsh(network shell on windows) to get the names of all networks
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
    decoded_data = data.decode('utf-8', errors="backslashreplace").split('\n') 

    # this function  can be used for network names and keys
    def filter_data(text_needed_to_be_contained,data_to_extract_from):
        result = []
        for line in data_to_extract_from:
      
            if text_needed_to_be_contained in line:
                """
                 netowrk profile line formart ↓
                 All User Profile : network_name
                 
                 netowrk key line format 
                 Key Content            : network_password
                 
                 so we can filter them in the same way!
                """
            	
                _ , needed_data = line.split(":")
                """
                    needed_data  contains a space at the beginning
                    and a '\r'(return) at the end
                    this step removes the space and the return
                """
                needed_data = needed_data[1:len(needed_data)-1]
                result.append(needed_data)
        return result

    profiles = filter_data("All User Profile", decoded_data)

    for profile in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
            decoded_splitted_result = results.decode('utf-8', errors="backslashreplace").split('\n')

            results = filter_data("Key Content",decoded_splitted_result)

            try:
                print ("{:<30}|  {:<}".format(profile, results[0]))
            except IndexError:
                print ("{:<30}|  {:<}".format(profile, ""))

        except subprocess.CalledProcessError:
            print ("{:<30}|  {:<}".format(profile, "ENCODING ERROR"))

if __name__ == "__main__":
    main()
