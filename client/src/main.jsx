import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Toaster } from 'sonner'
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './global-state/app/store.js';

import ChatLoader from './components/ui/ChatLoader.jsx';
import App from './App.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Toaster position="top-right" richColors />

    <Provider store={store}>
      <PersistGate loading={<ChatLoader/>} persistor={persistor}>
        <App />
      </PersistGate>
    </Provider>
  </StrictMode>,
)