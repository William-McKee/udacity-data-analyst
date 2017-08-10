# Pennsylvania Campaign Funds 2016

This project explores campaign contributions made to the Presidential Candidates from Pennsylvania donors made during the 2016 primary and general election seasons.

## Installation

Download **PA_Campaign_Funds_2016.rmd** file and open in RStudio.

If you do not have RStudio, download the open source RStudio desktop from [RStudio website](https://www.rstudio.com/products/RStudio/).

After installing RStudio, open RStudio and go to `File -> Open File` and select **PA_Campaign_Funds_2016.rmd**. The R-code base is shown in the upper left panel.  In the section `"{r echo=FALSE, Load_the_Data}"`, change `setwd()` to point to your working directory.

The associated data set is not included in this repository.  The data can be found on the [Federal Election Commisson page](http://classic.fec.gov/disclosurep/pnational.do).  Select the 2016 radio button near the top of the page. Go to right sidebar and click **"Export Contributor Data"** button.  Download PA.zip and uncompress in your working directory.

## Running the code

Once the data set is available, go into RStudio top-left panel and click `Run -> Run All Chunks Below`.

Once code is finished running, click on `Knit -> Knit to HTML` to create the HTML file.  The file should look just like the 
HTML file in this repository.