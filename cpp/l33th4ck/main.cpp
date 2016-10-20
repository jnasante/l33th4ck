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
int minRange = 1;
int maxRange = 10;

string addPrefix(string value) {
    return ID + value;
}

string getRandomWithPrefix() {
    return addPrefix(randomString);
}

int getK(string values[]) {
    int k = 0;
    while (k < values[0].length()) {
        if (values[0][k] != values[1][k]) {
            break;
        }
        
        k++;
    }
    
    return k * 4;
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
    int iterations = 0;
    int hare_steps = 0;
    int step_threshold = 2;
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
    
    return 0;
}
