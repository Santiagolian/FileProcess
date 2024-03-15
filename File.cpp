#include <fstream>
#include <iostream>
#include <vector>
#include <string>

using namespace std;
// string &processText(){

//     string text;
//     while(cin >> text){

//         return text;
//     }
// }

int main(){

    ifstream infile;
    ifstream infile1;
    ofstream outfile;
    // vector<string>::const_iterator it = files.begin();
    string ifile = "C:\\Users\\Administrator\\Desktop\\11.txt";
    string ifile1 = "C:\\Users\\Administrator\\Desktop\\13.txt";
    string ofile = "C:\\Users\\Administrator\\Desktop\\out.txt";
    
    infile.open(ifile);
    infile1.open(ifile1);
    outfile.open(ofile);
    outfile.close();
    outfile.open(ofile, ofstream::app);

    if(!infile or !infile1){
        cerr << "error: unable to open input file: " 
             << ifile << endl;
        return -1;
    }
    string s,s1;
    while(infile >> s && infile1 >> s1)
        // cout << s << endl  << s1 << endl; 
        outfile << s << endl  << s1 << endl;
    
    infile.close();
    infile1.close();
    outfile.close();
    
    cout << "读取11" << endl;
    return 0;
}