package app

import (
	"context"
	"testing"
)

func TestRun_Smoke(t *testing.T) {
	if err := Run(context.Background()); err != nil {
		t.Fatal(err)
	}
}
