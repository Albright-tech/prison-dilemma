import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import PrisonDilemmaGame from './components/PrisonDilemmaGame';
import Login from './components/Login';
import Register from './components/Register';
import { AuthProvider, useAuth } from './components/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<ProtectedRoute />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

const ProtectedRoute = () => {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? (
    <PrisonDilemmaGame />
  ) : (
    <Navigate to="/login" replace state={{ from: '/' }} />
  );
};

export default App;