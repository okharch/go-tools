// list sha256 for all the files from current directory
package main

import (
	"crypto/sha256"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
)

func sha256str(fileName string) string {
	f, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()
	var h = sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		log.Fatal(err)
	}
	return fmt.Sprintf("%x", h.Sum(nil))
}

func main() {
	files, err := ioutil.ReadDir(".")
	if err != nil {
		log.Fatal(err)
	}

	for _, file := range files {
		fmt.Println(sha256str(file.Name()), file.Name())
	}
}
