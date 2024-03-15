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
    string itagsPath = "C:\\Users\\Administrator\\Desktop\\11.txt";
    string iMtagsPath = "C:\\Users\\Administrator\\Desktop\\13.txt";
    string imfile = "C:\\Users\\Administrator\\Desktop\\out.txt";

    string otagsPath = "C:\\Users\\Administrator\\Desktop\\12.txt";
    string oMtagsPath = "C:\\Users\\Administrator\\Desktop\\14.txt";
    string omfile = "C:\\Users\\Administrator\\Desktop\\out1.txt";

    vector<string> strvec;
    strvec.push_back(itagsPath);
    strvec.push_back(iMtagsPath);
    strvec.push_back(imfile);

    strvec.push_back(oMtagsPath);
    strvec.push_back(otagsPath);
    strvec.push_back(omfile);
    for (size_t i = 0; i < 6; i++)
    {
        /* code */
    }
    int i = 0;
    while (i < 6)
    {
        /* code */
        infile.clear();
        infile1.clear();
        outfile.clear();
        infile.open(strvec[i]);
        infile1.open(strvec[i+1]);
        outfile.open(strvec[i+2]);
        outfile.close();
        outfile.open(strvec[i+2], ofstream::app);

        if(!infile or !infile1){
            cerr << "error: unable to open input file: " 
                << strvec[i] << endl;
            return -1;
        }
        string s,s1;
        while(infile >> s && infile1 >> s1)
            // cout << s << endl  << s1 << endl;   //去掉注释后会影响下一行
            outfile << s << endl  << s1 << endl;
        
        infile.close();
        infile1.close();
        outfile.close();
        i = i + 3;
        
    }
    
    cout << "读取11" << endl;
    return 0;
}