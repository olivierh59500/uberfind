#!/usr/bin/python
import os
import argparse
import re

__description__ = 'Quick script to parse trough files/folders recursively and search for a keyword.'
__author__ = 'bgx4k3p'
__version__ = '1.2'
__date__ = '2015/10/28'

""" SETTINGS
path - Path to search in recursively, default is the current directory
keywords - Strings to search for
file_ext - Specify file extensions to look in
results - Output file
chars - Number of characters to return before and after a keyword is found in a file
all_files - Look trough all files, no extensions filter
verbose - Enable verbosity
"""


# Function to return a list of file names in a given path recursively
def listAllFiles(path):

    flist = []

    # Walk trough all files and subdirectories
    for (dirname, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            # Append filename to list
            flist.append(os.path.join(dirname, filename))

    return flist


# Function to filter a list of file names with certain extensions
def filterFileTypes(filelist, extensions):

    filtered = []

    for f in filelist:

        # Split the extension from the path and normalise it to lowercase.
        ext = os.path.splitext(f)[-1].lower()

        # Check the file extension and append on the list if matching.
        if ext in extensions:
            filtered.append(f)

    return filtered


# Function to search for a keyword in an input file and write the results to an output file using REGEX
def searcherRegex(outfile, infile, lookup, n, v):

    writepath = True
    counter = 0

    with open(infile, 'r') as temp:
        for num, line in enumerate(temp, 1):

            # Strip whitespace characters at the end of the line
            line = line.rstrip()

            # Check each string on the lookup list
            for string in lookup:

                # Regex search with Ignorecase
                searchObj = re.finditer(string, line, re.M | re.I)

                if searchObj:
                    for match in searchObj:

                        # Find the start index of the keyword
                        start = match.span()[0]

                        # Find the end index of the keyword
                        end = match.span()[1]

                        # Truncate line to get only 'n' characters before and after the keyword
                        if match.span()[0]-n < 0:
                            tmp = line[0:end+n] + '\n'
                        else:
                            tmp = line[abs(start-n):abs(end+n)] + '\n'

                        # Write the file path once
                        if writepath:

                            # Verbose
                            if v:
                                print (os.path.realpath(infile))

                            outfile.write('=== FILE ====>>>   ' + os.path.realpath(infile) + '\n')
                            writepath = False
                            counter += 1

                        # Write the information and line number to output file
                        outfile.write('--> Found \"' + string + '\": Line ' + str(num) + '\n' + tmp + '\n')

    if counter == 1:
        outfile.write('\n\n')

    return counter


# MAIN
def main():
    # DEFAULT VALUES
    keywords = ['password', 'username']
    file_ext = ['.dll', '.xml', '.db', '.conf', '.ini', '.txt', '.dat', '.vbs', '.bat']
    results = 'results.txt'
    chars = 20
    path = os.getcwd()
    all_files = False
    verbose = False

    # Handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action='store', help="Specify path to search in", dest="path")
    parser.add_argument("-k", action='append', help="Specify keywords to search for", dest="keywords")
    parser.add_argument("-e", action='append', help="Specify file types to search in", dest="extensions")
    parser.add_argument("-r", action='store', help="Specify results output file, default 'results.txt'", dest="results")
    parser.add_argument("-n", action='store', help="Number of characters to return before and after a keyword",
                        dest="chars")
    parser.add_argument("-a", action='store_true', help="Search ALL files, no filter", dest="all_files")
    parser.add_argument("-v", "--verbose", action='store_true', help="Enable verbosity", dest="verbose")
    args = parser.parse_args()

    if args.verbose:
        verbose = args.verbose
    if args.path:
        path = args.path
    if args.keywords:
        keywords = args.keywords
    if args.extensions:
        file_ext = args.extensions
    if args.results:
        results = args.results
    if args.chars:
        chars = args.chars
    if args.all_files:
        print "Searching ALL files!"
        all_files = args.all_files

    # Processing
    with open(results, 'w') as r:

        print '\n'
        print '$$\   $$\ $$\                           $$$$$$$$\ $$\                 $$\ '
        print '$$ |  $$ |$$ |                          $$  _____|\__|                $$ |'
        print '$$ |  $$ |$$$$$$$\   $$$$$$\   $$$$$$\  $$ |      $$\ $$$$$$$\   $$$$$$$ |'
        print '$$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$$$$\    $$ |$$  __$$\ $$  __$$ |'
        print '$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|$$  __|   $$ |$$ |  $$ |$$ /  $$ |'
        print '$$ |  $$ |$$ |  $$ |$$   ____|$$ |      $$ |      $$ |$$ |  $$ |$$ |  $$ |'
        print '\$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      $$ |      $$ |$$ |  $$ |\$$$$$$$ |'
        print ' \______/ \_______/  \_______|\__|      \__|      \__|\__|  \__| \_______|'
        print '\n'
        print "Search path:", path
        print "Keywords:", ' '.join(str(keyword) for keyword in keywords)
        print "File extensions:", ' '.join(str(ext) for ext in file_ext)
        print "Number of characters before and after a keyword:", chars
        #print "Results file:", args.results

        # Counter for the number of files containing a keyword
        count = 0

        # Get a list of all files in the path recursively
        files = listAllFiles(path)

        # Enable file extensions filter or search all files
        if all_files is False:
            files_to_search = filterFileTypes(files, file_ext)
        else:
            files_to_search = files

        # Perform search
        for f in files_to_search:
            count += searcherRegex(r, f, keywords, chars, verbose)

        print "Searched through", len(files_to_search), 'files.'
        print "Found keyword in", count, 'files.'
        print "For more details, check the results file:", os.path.realpath(results)
    r.close()


if __name__ == '__main__':
    main()
