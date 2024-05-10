import React, { useState } from "react";
import { add, remove } from "../webapi/exchanges";

import Button from "../components/Button";
import ErrorModal from "../components/errorModal";
import FieldSelect from "../components/reusables/FieldSelect";
import FieldSwitch from "../components/reusables/FieldSwitch";
import Input from "../components/reusables/Input";
import SuccessModal from "../components/successModal";
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
  const [successModalOpen, setSuccessModalOpen] = useState(false)
  const [errorModalMessage, setErrorModalMessage] = useState("")
  const [successModalMessage, setSuccessModalMessage] = useState("")
  const [errorModalOpen, setErrorModalOpen] = useState(false)
  const [testingNetwork, setTestingNetwork] = useState(false)
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [alias, setAlias] = useState("");
  const options = [{ value: "binance", label: "Binance" }];

  const [loading, setLoading] = useState(false);

  const handleCloseSuccessModal = () => {
    setSuccessModalOpen(false);
  }

  const handleSelectChange = (name, value) => {
    setSelectedOption(value);
  };

  const handleAddClick = () => {
    setLoading(true);
    add({
      exchange_name: selectedOption.label,
      api_key: apiKey,
      api_secret: apiSecret,
      alias: alias,
      testing_network: testingNetwork,
    })
      .then(() => {setLoading(false); setSuccessModalMessage("Provider saved correctly!"); setSuccessModalOpen(true);})
      .catch(() => {setLoading(false); setErrorModalMessage("An error has occured while adding the provider. Please try again later!"); setErrorModalOpen(true)});
  };

  const handleDeleteClick = () => {
    setLoading(true);
    remove({
      exchange_name: selectedOption.label,
      api_key: apiKey,
      api_secret: apiSecret,
      alias: alias,
      testing_network: testingNetwork,
    })
      .then(() => {setLoading(false); setSuccessModalMessage("Provider deleted correctly!"); setSuccessModalOpen(true);})
      .catch(() => {setLoading(false); setErrorModalMessage("The provider you are trying to delete does not exist!"); setErrorModalOpen(true)});
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
              <h2 style={{ textAlign: "center" }}>Write the Alias of your provider:</h2>
              <Input
                width="30rem"
                onChange={(e) => setAlias(e.target.value)}
              />
              <h2 style={{ textAlign: "center" }}>Testing Network</h2>
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                }}
              >
              <FieldSwitch
                name={"TestingNetworkSwitch"}
                value={testingNetwork}
                onChange={()=> setTestingNetwork(!testingNetwork)}
              />
              </div>
              <div
                style={{
                  marginTop: "1rem",
                  display: "flex",
                  justifyContent: "space-between",
                  paddingRight: "2rem",
                  paddingLeft: "2rem",
                }}
              >
                <Button
                  text={"DELETE"}
                  height={40}
                  width={100}
                  onClick={handleDeleteClick}
                  loading={loading}
                />
                <Button
                  text={"ADD"}
                  height={40}
                  width={100}
                  onClick={handleAddClick}
                  loading={loading}
                />
                <SuccessModal
                  isOpen={successModalOpen}
                  message={successModalMessage}
                  onClose={handleCloseSuccessModal}
                />
                <ErrorModal
                  isOpen={errorModalOpen}
                  message={errorModalMessage}
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
