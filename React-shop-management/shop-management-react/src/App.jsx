import React, { useState } from 'react';
import { 
  Container,
  Typography,
  Paper,
  Box,
  Tabs,
  Tab
} from '@mui/material';
import { Build, CalendarToday } from '@mui/icons-material';
import Reparacoes from './Reparacoes';
import Appointments from './Appointments';

export default function App() {
  const [activeTab, setActiveTab] = useState('reparacoes');

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Título */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          PrimeTech – Gestão
        </Typography>
      </Box>

      {/* Tabs */}
      <Paper sx={{ mb: 4 }}>
        <Tabs 
          value={activeTab}
          onChange={handleTabChange}
          variant="fullWidth"
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab 
            value="reparacoes" 
            label="Reparações" 
            icon={<Build />} 
            iconPosition="start" 
          />
          <Tab 
            value="appointments" 
            label="Agendamentos" 
            icon={<CalendarToday />} 
            iconPosition="start" 
          />
        </Tabs>
      </Paper>

      {/* Conteúdo */}
      <Paper sx={{ p: 4 }}>
        {activeTab === 'reparacoes' && <Reparacoes />}
        {activeTab === 'appointments' && <Appointments />}
      </Paper>
    </Container>
  );
}
