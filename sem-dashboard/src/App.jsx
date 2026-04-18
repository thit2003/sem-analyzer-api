import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { UploadCloud, Trophy, AlertCircle } from 'lucide-react'
import './App.css' // Assuming standard Vite CSS setup

function App() {
  const [file, setFile] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setError(null)
  }

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file first.")
      return
    }

    setLoading(true)
    setError(null)

    // Prepare the file to be sent as FormData (just like in Postman)
    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("https://sem-analyzer-api.onrender.com/api/analyze", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Failed to analyze data. Make sure it's a valid Google Ads CSV.")
      }

      const data = await response.json()
      setResults(data.data) // Store the nested data object
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Helper to format the backend dictionary into an array for Recharts
  const formatChartData = (metrics) => {
    return Object.entries(metrics).map(([adName, data]) => ({
      name: adName,
      CVR: data.CVR,
      CTR: data.CTR
    }))
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', fontFamily: 'system-ui' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>📊 SEM A/B Test Analyzer</h1>

      {/* Upload Section */}
      <div style={{ border: '2px dashed #ccc', padding: '2rem', textAlign: 'center', borderRadius: '8px', marginBottom: '2rem' }}>
        <UploadCloud size={48} color="#666" style={{ marginBottom: '1rem' }} />
        <h3>Upload Google Ads Data</h3>
        <p style={{ color: '#666', marginBottom: '1rem' }}>CSV format containing: Ad Name, Impressions, Clicks, Conversions</p>
        <input type="file" accept=".csv" onChange={handleFileChange} style={{ marginBottom: '1rem' }} />
        <br />
        <button 
          onClick={handleUpload} 
          disabled={loading}
          style={{ padding: '10px 20px', background: '#0070f3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '16px' }}
        >
          {loading ? "Analyzing..." : "Analyze Campaign"}
        </button>
        {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
      </div>

      {/* Results Section */}
      {results && (
        <div>
          {/* The Winner Banner */}
          <div style={{ 
            background: results.analysis.is_significant ? '#dcfce7' : '#fef08a', 
            padding: '1.5rem', 
            borderRadius: '8px', 
            marginBottom: '2rem',
            display: 'flex',
            alignItems: 'center',
            gap: '1rem'
          }}>
            {results.analysis.is_significant ? <Trophy size={32} color="#166534" /> : <AlertCircle size={32} color="#854d0e" />}
            <div>
              <h2 style={{ margin: 0, color: results.analysis.is_significant ? '#166534' : '#854d0e' }}>
                {results.analysis.is_significant ? `Winner: ${results.analysis.winner}` : "No Statistically Significant Winner"}
              </h2>
              <p style={{ margin: '5px 0 0 0', color: '#444' }}>
                P-Value: {results.analysis.p_value} (Industry standard requires &lt; 0.05)
              </p>
            </div>
          </div>

          {/* Visualization */}
          <h3>Conversion Rate (CVR) Comparison</h3>
          <div style={{ width: '100%', height: '300px', background: '#f9fafb', padding: '1rem', borderRadius: '8px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={formatChartData(results.performance_metrics)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis unit="%" />
                <Tooltip />
                <Legend />
                <Bar dataKey="CVR" fill="#3b82f6" name="Conversion Rate (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}

export default App