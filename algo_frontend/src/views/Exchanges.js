import React, { useState } from "react";

import Button from "../components/Button";
import FieldSelect from "../components/reusables/FieldSelect";
import Input from "../components/reusables/Input";
import View from "../components/reusables/View";
import styled from "styled-components";

const ExchangesStyle = styled.div`
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  margin-top: 40px;
  margin-bottom: 40px;
`;

const Exchanges = () => {
  const [selectedOption, setSelectedOption] = useState("");
  const options = [{ value: "binance", label: "Binance" }];

  const handleSelectChange = (e) => {
    setSelectedOption(e.value);
  };
  return (
    <>
      <View
        title="Exchanges"
        content={
          <ExchangesStyle>
            <form>
              <h2 style={{ textAlign: "center" }}>Select your provider:</h2>
              <FieldSelect
                value={selectedOption}
                name="selectProvider"
                onChange={handleSelectChange}
                options={options}
                multiple={false}
                width="30rem"
              />
              <h2 style={{ textAlign: "center" }}>Write your API key:</h2>
              <Input width="30rem" />
              <h2 style={{ textAlign: "center" }}>Write your API secret:</h2>
              <Input width="30rem" type={"password"} />
              <div
                style={{
                  marginTop: "2rem",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <Button text={"SAVE"} height={40} width={100} />
              </div>
            </form>
          </ExchangesStyle>
        }
      />
    </>
  );
};

export default Exchanges;
