import "../styles/tradesView.css";

import React from "react";

const TradesView = () => {
  const hardcodedTrades = [
    {
      dateTime: "2023-12-15 10:30 AM",
      asset: "AAPL",
      amount: 10,
      type: "Bought",
    },
    {
      dateTime: "2023-12-16 02:45 PM",
      asset: "GOOGL",
      amount: 5,
      type: "Sold",
    },
  ];

  return (
    <div className="trades-view-container">
      <table className="trades-table">
        <thead>
          <tr>
            <th>Date & Time</th>
            <th>Asset</th>
            <th>Amount</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {hardcodedTrades.map((trade, index) => (
            <tr key={index}>
              <td>{trade.dateTime}</td>
              <td>{trade.asset}</td>
              <td>{trade.amount}</td>
              <td className={trade.type.toLowerCase()}>{trade.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TradesView;
