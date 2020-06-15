## File_Pal

Note: If the progress bar gets stuck due to an error you can click ctrl+c to remove, but be careful not to click into the cmd/shell window and press ctrl+c since it will close the whole application.

This tool is used to load large CSV files and search multiple files with the same criteria.

### Getting Started

![File_pal](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/File_Pal.png)

This is one of my first tutorial write ups so please go easy on me. (But i'd appreciate any constructive feedback)

![File_pal_Options](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/File_Pal_Options.png)

First we'd want to click File>Options.

![FP_Search_Output](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_Search_Output.png)

Then we'd click inside the "Click Here" button on the pop-up window.

![FP_SO_General](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_SO_General.png)

After that we'll want to choose "General".

![FP_SO_General2](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_SO_General2.png)

Now we can enter some general file output preferences. (Don't forget to click Save) I would also recommend clicking the "Output Dir" button so that we can set where our files will be generated.

![FP_SO_G_OutputDir](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_SO_G_OutputDir.png)

I'd also recommend creating a folder on your desktop named "File_Pal_Output" or "Trash_Stuff" so that you see it often and can get reminded to delete these output files. (I'll be adding an Auto-Delete checkbutton to the main window at one point)

![FP_SO_G_OutputDir2](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_SO_G_OutputDir2.png)

Here is my output folder selected.

![FP_SO_General3](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_SO_General3.png)

And here's an updated picture of File>Options>Search_Output>General to show my new output location is set.

![File_Open_SelectFile](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/File_Open_SelectFile.png)

Now we can start opening our files by going to File>Open>Select_File. I would suggest only using this application with CSV files for now. I set a restriction on xlsx files to only allow up to 2MB because they open super slow right now. Adding support for larger xls files is my next objective. (And then i'll be thinking about adding SQL functionality)

![FP_Select_Files](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_Select_Files.png)

With the "Select_File" pop-up we can select 1+ files from a directory.

![FP_Open_Files](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_Open_Files.png)

This image shows (in the background shell window) that it took 8-9.2 seconds to load three 60MB CSV files. It opened them in my windows Virtual Machine from another location on my server (and the files don't contain a lot of data), so your open times may differ.

![FP_Headers](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_Headers.png)

Now if it's your first time using the application i'd suggest clicking on one of the "Headers" buttons next to one of the files. It will generate another pop-up with Headers associated with that file. If the headers aren't seperated like they are in this image then there is a chance our File input delimiter is set incorrectly. You can change this by going to File>Options>File_Input>General and then setting the delimiter to match your file. (And don't forget to click save before leaving) Soon i'll create a more in depth tutorial on what the rest of the settings are supposed to do for file Input and Search Output.

In this pop-up we can select a header to set in our main window by clicking one of the headers on the left or go deeper to see what results may be available under that header by selecting "Results within Column" on the right.

![FP_Headers](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_Headers.png)

If you selected "Results within Column" then you'll get a list of total results per value. You can click on these values to add them to your search items.

![FP_w_Search_Criteria](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/FP_w_Search_Criteria.png)

Now lets close the "Headers" pop-up. If you selected values (or entered them manually) you can click search or press "Enter" and let the application do it's thing. It will search in the order the files are listed on the main screen going from top down. If they opened in the incorrect order you can click the "Sort Files" button, enter the desired order, and then click "Save Order".

![Sort_Files](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/Sort_Files.png)

If you choose to change the search order for your files and you clicked "Sort Files" you will be presented with an input box to enter the order you want. If you have more than ten files you will want to use double digits for the first 9 numbers as well, for some reason it can impact the sort if the digit amount isn't the same. (e.g. 01 02 03 04 05 06 07 08 09 10 11 12...)

When you are ready and have clicked Search (or pressed Enter) the application will do it's thing. Another note is if you don't want the search to search a specific file you can unclick the check box next to the file.

![Search_Output](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/Search_Output.png)

After the application has done it's searching, if you left the "Auto Open" box checked on the main screen then the output file will automatically open in your preferred spreadsheet software.

![Copy_From_Output](https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/pics/Copy_From_Output.png)

If you are like me and work out of the same files all day then you can use these output files (or the original files) to copy your search headers and item(s) right into the application. You don't have to worry about the extra tabs that are copied from spreadsheets when you want to copy your header or Search item(s) from there, the application will remove and/or split them for you. And you don't have to worry about deleting duplicate search items from your search items since the application will do that for you too. But if you are searching by more than 500 items then i'd suggest removing duplicates in your spreadsheet software before copying them into the application. I'd also suggest limiting your Search Items to be less than 6000. When you start pasteing 1000+ items into the "Search Item(s)" input box it can take a little while for them all to paste, and the search itself will likely take a while. Once i add SQL functionality searching this amount will go faster (from SQL database searches). You probably wont often be searching by 1000+ items but it is nicer to filter one file with just relevant data in a spreadsheet software than it is to have to search multiple files. 

Please let me know if you have questions, suggestions, or would like my help automating some boring stuff! I'll try to get the information added for the extra Search Output and File input options soon!

scionsamurai@yahoo.com
