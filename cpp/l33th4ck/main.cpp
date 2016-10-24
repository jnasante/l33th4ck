//
//  main.cpp
//  l33th4ck
//
//  Created by Joseph Asante on 10/17/16.
//  Copyright © 2016 josephasante. All rights reserved.
//

#include <iostream>
#include <sstream>
#include <fstream>
#include <map>
#include <string>
#include "sha3.h"

using namespace std;

string ID = "112901008";
string fileName = "h4ck.txt";
string randomString = "A6f7Dy34ez";

int kMax = 0;
string kHashes[] = { "", "" };
map<string, string> kMap;

string addPrefix(string value) {
    return ID + value;
}

string getRandomWithPrefix() {
    return addPrefix(randomString);
}

// This method was taken from here: http://www.cplusplus.com/forum/beginner/41657/
string convertHexToBinary (string sHex)
{
    string sReturn = "";
    for (int i = 0; i < sHex.length (); ++i)
    {
        switch (sHex [i])
        {
            case '0': sReturn.append ("0000"); break;
            case '1': sReturn.append ("0001"); break;
            case '2': sReturn.append ("0010"); break;
            case '3': sReturn.append ("0011"); break;
            case '4': sReturn.append ("0100"); break;
            case '5': sReturn.append ("0101"); break;
            case '6': sReturn.append ("0110"); break;
            case '7': sReturn.append ("0111"); break;
            case '8': sReturn.append ("1000"); break;
            case '9': sReturn.append ("1001"); break;
            case 'a': sReturn.append ("1010"); break;
            case 'b': sReturn.append ("1011"); break;
            case 'c': sReturn.append ("1100"); break;
            case 'd': sReturn.append ("1101"); break;
            case 'e': sReturn.append ("1110"); break;
            case 'f': sReturn.append ("1111"); break;
        }
    }
    return sReturn;
}

int getK(string values[]) {
    int k = 0;
    string bitValues[] = { convertHexToBinary(values[0]), convertHexToBinary(values[1]) };
    while (k < bitValues[0].length()) {
        if (bitValues[0][k] != bitValues[1][k]) {
            break;
        }
        
        k++;
    }
    
    return k;
}

void printResults(int k) {
    string hash1 = kHashes[0];
    string hash2 = kHashes[1];

    string value1 = kMap[hash1];
    string value2 = kMap[hash2];
    
    std::ostringstream oss;
    oss << "FOUND NEW K: " << k << endl;
    oss << "Strings: " << value1 << ", " << value2 << endl;
    oss << "Hashes: " << hash1 << ", " << hash2 << endl;
    string fanfare = oss.str();
    
    // Print to console
    cout << fanfare << endl;
    
    // Write to file
    ofstream logFile;
    logFile.open(fileName);
    logFile.flush();
    logFile << fanfare << endl;
    logFile.close();
}

void foundNewK(int k, string hashArray[]) {
    kMax = k;
    kHashes[0] = hashArray[0];
    kHashes[1] = hashArray[1];
    printResults(k);
}

void checkKResult(string tortoise, string tortoiseHash, string hare, string hareHash) {
    string hashArray[] = { tortoiseHash, hareHash };
    int k = getK(hashArray);
    if (k > kMax) {
        kMap[tortoiseHash] = tortoise;
        kMap[hareHash] = hare;
        foundNewK(k, hashArray);
    }
}

void brent() {
    SHA3 sha3 (SHA3 :: Bits224);
    
    string seed = getRandomWithPrefix();
    long iterations = 0;
    long hare_steps = 0;
    long step_threshold = 2;
    string tortoise = seed;
    string tortoiseHash = sha3(seed);
    string hare = seed;
    string hareHash = sha3(seed);
    
    while (true) {
        if (iterations % 1000000000 == 0) {
            cout << "\nIteration: " << iterations << "\n" << endl;
        }
        
        hare = addPrefix(hareHash);
        hareHash = sha3(hare);
        hare_steps++;
        
        checkKResult(tortoise, tortoiseHash, hare, hareHash);

        if (hare_steps == step_threshold) {
            hare_steps = 0;
            step_threshold *= 2;
            tortoise = hare;
            tortoiseHash = hareHash;
            cout << "Step threshold: " << step_threshold << "\n" << endl;
        }
        
        iterations++;
    }
}

void pollardRho() {
    SHA3 sha3 (SHA3 :: Bits224);
    
    string seed = getRandomWithPrefix();
    int iterations = 0;
    string tortoise = seed;
    string tortoiseHash = sha3(seed);
    string hare = seed;
    string hareHash = sha3(seed);
    
    while (true) {
        if (iterations % 1000000000 == 0) {
            cout << "\nIteration: " << iterations << "\n" << endl;
        }
        
        for (int i = 0; i < 2; i++) {
            hare = addPrefix(hareHash);
            hareHash = sha3(hare);
            
            checkKResult(tortoise, tortoiseHash, hare, hareHash);
        }

        tortoise = addPrefix(tortoiseHash);
        tortoiseHash = sha3(tortoise);
        
        iterations++;
    }
}

int main(int argc, const char * argv[]) {
    cout << "Hacking into mainframe..." << endl;
    
    std::ostringstream oss;
    oss << argv[1] << "_h4ck.txt";
    fileName = oss.str();
    
    randomString = argv[2];
    
//    pollardRho();
    brent();
    
//    string hashArray[] = { "0e5928cb450b2e232923a2c4dd1d0d7a068e2720c05f76a5e8808a02", "0e5928cb455c27708d53abebf845ab7c6d0ed900a9a278161ab38f09" };
//    cout << getK(hashArray) << endl;
    
    return 0;
}
