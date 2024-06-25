import React from 'react';
import SendSceneParamsForm from './components/SendSceneParamsForm';
import RegisterUserForm from './components/RegisterUserForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>FastAPI + Kafka Example</h1>
      </header>
      <main>
        <SendSceneParamsForm />
        <RegisterUserForm />
      </main>
    </div>
  );
}

export default App;
