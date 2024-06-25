import React, { useState } from 'react';
import axios from 'axios';

const SendSceneParamsForm = () => {
  const [asset, setAsset] = useState('');
  const [strategy, setStrategy] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [cash, setCash] = useState('');
  const [commission, setCommission] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/send_scene_params/', {
        asset,
        strategy,
        start_date: startDate,
        end_date: endDate,
        cash: parseFloat(cash),
        commission: parseFloat(commission)
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error sending scene parameters');
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Send Scene Parameters</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Asset:
          <input type="text" value={asset} onChange={(e) => setAsset(e.target.value)} required />
        </label>
        <label>
          Strategy:
          <input type="text" value={strategy} onChange={(e) => setStrategy(e.target.value)} required />
        </label>
        <label>
          Start Date:
          <input type="text" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
        </label>
        <label>
          End Date:
          <input type="text" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
        </label>
        <label>
          Cash:
          <input type="number" value={cash} onChange={(e) => setCash(e.target.value)} required />
        </label>
        <label>
          Commission:
          <input type="number" value={commission} onChange={(e) => setCommission(e.target.value)} required />
        </label>
        <button type="submit">Send Scene Parameters</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SendSceneParamsForm;
