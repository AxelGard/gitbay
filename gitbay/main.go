package main

import (
	"fmt"
	"io/ioutil"
	"log"

	shell "github.com/ipfs/go-ipfs-api"
)

func main() {
	sh := shell.NewShell("localhost:5001")

	cid := "QmT78zSuBmuS4z925WZfrqQ1qHaJ56DQaTfyMUF7F8ff5o"

	reader, err := sh.Cat(cid)
	if err != nil {
		log.Fatal(err)
	}

	data, err := ioutil.ReadAll(reader)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Data: %s\n", data)
}
