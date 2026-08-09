package main

import (
	"context"
	"log"

	"demo-service/internal/app"
)

func main() {
	ctx := context.Background()
	if err := app.Run(ctx); err != nil {
		log.Fatalf("exit error: %v", err)
	}
}
