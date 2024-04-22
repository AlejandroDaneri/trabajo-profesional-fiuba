package pythonservice

import (
	"sync"
)

var instance IService
var once sync.Once

func GetInstance() IService {
	once.Do(func() {
		instance = NewService()
	})
	return instance
}

type PythonService struct {
}

func NewService() IService {
	return &PythonService{}
}

type IService interface {
	GetBacktesting() error
}

func (s *PythonService) GetBacktesting() error {
	return nil
}
