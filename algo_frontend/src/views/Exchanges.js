import React, { useState } from "react";

import Button from "../components/Button";
import ErrorModal from "../components/errorModal";
import FieldSelect from "../components/reusables/FieldSelect";
import Input from "../components/reusables/Input";
import SuccessModal from "../components/successModal";
import View from "../components/reusables/View";
import { add } from "../webapi/exchanges";
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
  const [successModalOpen, setSuccessModalOpen] = useState(false)
  const [errorModalOpen, setErrorModalOpen] = useState(false)
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const options = [{ value: "binance", label: "Binance" }];

  const [loading, setLoading] = useState(false);

  const handleCloseSuccessModal = () => {
    setSuccessModalOpen(false);
  }

  const handleSelectChange = (name, value) => {
    setSelectedOption(value);
  };

  const handleSaveClick = () => {
    setLoading(true);
    add({
      exchange_name: selectedOption.label,
      api_key: apiKey,
      api_secret: apiSecret,
    })
      .then(() => {setLoading(false); setSuccessModalOpen(true);})
      .catch(() => {setLoading(false); setErrorModalOpen(true)});
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
              <Input
                width="30rem"
                onChange={(e) => setApiKey(e.target.value)}
              />
              <h2 style={{ textAlign: "center" }}>Write your API secret:</h2>
              <Input
                width="30rem"
                type={"password"}
                onChange={(e) => setApiSecret(e.target.value)}
              />
              <div
                style={{
                  marginTop: "2rem",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <Button
                  text={"SAVE"}
                  height={40}
                  width={100}
                  onClick={handleSaveClick}
                  loading={loading}
                />
                <SuccessModal
                  isOpen={successModalOpen}
                  message="Provider saved correctly!"
                  onClose={handleCloseSuccessModal}
                />
                <ErrorModal
                  isOpen={errorModalOpen}
                  message={"An error has occured. Please try again later!"}
                  onClose={() => setErrorModalOpen(false)}
                />
              </div>
            </form>
          </ExchangesStyle>
        }
      />
    </>
  );
};

export default Exchanges;
