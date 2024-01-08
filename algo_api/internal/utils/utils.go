package utils

import (
	"encoding/json"
	"fmt"
)

func StructToMap(value interface{}) (map[string]interface{}, error) {
	if res, ok := value.(map[string]interface{}); ok {
		return res, nil
	}

	valueBytes, err := json.Marshal(value)
	if err != nil {
		return nil, fmt.Errorf("error marshalling struct: %w", err)
	}

	var valueMap map[string]interface{}
	err = json.Unmarshal(valueBytes, &valueMap)
	if err != nil {
		return nil, fmt.Errorf("error unmarshalling struct: %w", err)
	}

	return valueMap, nil
}

func ToPrettyPrint(m interface{}) string {
	b, err := json.MarshalIndent(m, "", "    ")
	if err == nil {
		return string(b)
	}
	return ""
}
