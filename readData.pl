#!/usr/bin/perl

# ###########################################################################
# This program can help to convert data in the .ltp file format from
# LatisPro into a text file.
#
# In fact, the latisPro file is in XML format. It seems the structure
# can vary. Once you know the structure, you can get the raw data.
#
# Then the raw data needs to be converted from hexadecimal into 
# a double precision floating point. Note, the hex string first needs
# to be reversed.
# ###########################################################################

# Use the XML package to read the file
use XML::Simple;
use Data::Dumper;

# Create a temp file that only contains the first block in the XML file
my $tmp_file = "$$.tmp";
open( my $fh1, "<:encoding(UTF-16)", $ARGV[0] );
open( my $fh2, ">", $tmp_file );
while (<$fh1>) {
   print $fh2 $_;
   if (/\/BLOC-COURBES/) { last; }
}
close $fh1;
close $fh2;

# Here we read in the XML file, that is passed as an argument on the command line
my $xml = new XML::Simple;
my $data = $xml->XMLin($tmp_file);


# Uncomment the line below to see the structure of your file
#print Dumper($data);

# Modify this line, to point to the data you want to extract
my $raw_data = $data->{LESCOURBES}->{C}->{C0}->{DATAY}->{DonneesY}->{DONNEES};

# This is a sample of test data that contains the values:
# 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 0 0
# and can be used for debug
#my $raw_data = "3FF000000000000040000000000000004008000000000000401000000000000040140000000000004018000000000000401C00000000000040200000000000004022000000000000402400000000000040260000000000004028000000000000402A000000000000402C000000000000402E000000000000403000000000000000000000000000000000000000000000";


#print $raw_data,"\n";

# Get the length of the raw data
my $len = length($raw_data);

# Split the data into chunks of 16 characters (16 bytes)
for( my $i=0 ; $i<($len/16) ; $i++) {
   my $value = substr( $raw_data, $i*16, 16);

   # Reverse the string
   my $reverse = "";
   for( my $j=15 ; $j>=0 ; $j-- ) {
       $reverse .= substr($value,$j,1);
   }

   # Convert the hext to binary
   my $binary = pack("h16",$reverse);
   # Convert the binary to a double precision floating point
   my $fl = unpack("d", $binary);

   # Print it
   print "$fl\n";
}

# Remove the temporary file
unlink($tmp_file);
