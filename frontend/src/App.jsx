import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE_URL = "https://vexa-ai-7rde.onrender.com";

function App() {
  // ==========================================
  // STATE
  // ==========================================

  const [leads, setLeads] = useState([]);
  const [selectedLead, setSelectedLead] = useState(null);

  const [currentPage, setCurrentPage] = useState("dashboard");

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [discovering, setDiscovering] = useState(false);

  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const [searchTerm, setSearchTerm] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("ALL");


  // ==========================================
  // FETCH LEADS
  // ==========================================

  const fetchLeads = async () => {
    try {
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/api/leads/`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch leads");
      }

      const data = await response.json();

      setLeads(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (err) {
      console.error(
        "Error fetching leads:",
        err
      );

      setError(
        "Unable to load leads from the backend."
      );

    } finally {
      setLoading(false);
    }
  };


  // ==========================================
  // INITIAL LOAD
  // ==========================================

  useEffect(() => {
    fetchLeads();
  }, []);


  // ==========================================
  // REFRESH LEADS
  // ==========================================

  const refreshLeads = async () => {
    setRefreshing(true);
    setError("");
    setSuccessMessage("");

    await fetchLeads();

    setRefreshing(false);
  };


  // ==========================================
  // RUN DISCOVERY
  // ==========================================

  const runDiscovery = async () => {
    if (discovering) {
      return;
    }

    setDiscovering(true);
    setError("");
    setSuccessMessage("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/discovery/run`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Discovery request failed"
        );
      }

      const result = await response.json();

      console.log(
        "Discovery result:",
        result
      );


      // --------------------------------------
      // REFRESH LEADS
      // --------------------------------------

      await fetchLeads();


      // --------------------------------------
      // SUCCESS MESSAGE
      // --------------------------------------

      const discoveredCount =
        result.leads_found ??
        result.leads_saved ??
        0;

      setSuccessMessage(
        `Discovery completed successfully. ${discoveredCount} leads are now available.`
      );


      // --------------------------------------
      // MOVE TO LEADS PAGE
      // --------------------------------------

      setCurrentPage("leads");

    } catch (err) {
      console.error(
        "Discovery error:",
        err
      );

      setError(
        "Discovery failed. Please try again."
      );

    } finally {
      setDiscovering(false);
    }
  };


  // ==========================================
  // OPEN LEAD DETAILS
  // ==========================================

  const openLeadDetails = async (lead) => {
    setSelectedLead(lead);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/leads/${lead.id}`
      );

      if (!response.ok) {
        return;
      }

      const detailedLead =
        await response.json();

      setSelectedLead(
        detailedLead
      );

    } catch (err) {
      console.error(
        "Unable to load lead details:",
        err
      );
    }
  };


  // ==========================================
  // CLOSE LEAD DETAILS
  // ==========================================

  const closeLeadDetails = () => {
    setSelectedLead(null);
  };


  // ==========================================
  // NAVIGATION
  // ==========================================

  const goToPage = (page) => {
    setCurrentPage(page);
    setSelectedLead(null);
    setSuccessMessage("");
  };


  // ==========================================
  // DASHBOARD STATISTICS
  // ==========================================

  const totalLeads = leads.length;

  const highPriorityLeads =
    leads.filter(
      (lead) =>
        String(
          lead.priority || ""
        ).toLowerCase() === "high"
    ).length;


  const averageScore =
    leads.length > 0
      ? Math.round(
          leads.reduce(
            (total, lead) =>
              total +
              Number(
                lead.opportunity_score || 0
              ),
            0
          ) / leads.length
        )
      : 0;


  const gamingSignals =
    leads.filter(
      (lead) =>
        lead.gaming_signal === true
    ).length;


  // ==========================================
  // FILTER LEADS
  // ==========================================

  const filteredLeads = useMemo(() => {
    return leads.filter((lead) => {

      const brand =
        String(
          lead.brand_name || ""
        ).toLowerCase();

      const search =
        searchTerm
          .toLowerCase()
          .trim();

      const matchesSearch =
        brand.includes(search);

      const leadPriority =
        String(
          lead.priority || ""
        ).toUpperCase();

      const matchesPriority =
        priorityFilter === "ALL" ||
        leadPriority ===
          priorityFilter;

      return (
        matchesSearch &&
        matchesPriority
      );
    });
  }, [
    leads,
    searchTerm,
    priorityFilter
  ]);


  // ==========================================
  // PRIORITY CLASS
  // ==========================================

  const getPriorityClass = (
    priority
  ) => {

    const value =
      String(
        priority || ""
      ).toLowerCase();

    if (value === "high") {
      return "priority-high";
    }

    if (value === "medium") {
      return "priority-medium";
    }

    return "priority-low";
  };


  // ==========================================
  // SIGNAL STATUS
  // ==========================================

  const getSignalText = (value) => {
    return value ? "Yes" : "No";
  };


  // ==========================================
  // DASHBOARD
  // ==========================================

  const renderDashboard = () => {

    const priorityLeads =
      [...leads]
        .sort(
          (a, b) =>
            Number(
              b.opportunity_score || 0
            ) -
            Number(
              a.opportunity_score || 0
            )
        )
        .slice(0, 5);


    return (
      <div className="page-content">

        {/* HEADER */}

        <div className="page-header">

          <div>

            <h1>
              Sales Intelligence Dashboard
            </h1>

            <p>
              Discover and prioritize potential
              gaming sponsorship opportunities.
            </p>

          </div>


          <button
            className="discovery-button"
            onClick={runDiscovery}
            disabled={discovering}
          >

            {discovering
              ? "Discovering..."
              : "Run Discovery"}

          </button>

        </div>


        {/* DISCOVERY STATUS */}

        {discovering && (
          <div className="discovery-status-box">

            <div className="status-spinner">
              ⟳
            </div>

            <div>

              <strong>
                Discovery engine is running
              </strong>

              <p>
                Searching recent news and
                analyzing potential leads...
              </p>

            </div>

          </div>
        )}


        {/* SUCCESS */}

        {successMessage && !discovering && (

          <div className="success-message">

            <span>
              ✓
            </span>

            {successMessage}

          </div>

        )}


        {/* ERROR */}

        {error && (

          <div className="error-message">

            <span>
              !
            </span>

            {error}

          </div>

        )}


        {/* LAST UPDATED */}

        <div className="last-updated">

          Last updated:{" "}

          {new Date().toLocaleString()}

        </div>


        {/* KPI CARDS */}

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-label">
              TOTAL LEADS
            </div>

            <div className="stat-value">
              {totalLeads}
            </div>

            <div className="stat-description">
              Discovered opportunities
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-label">
              HIGH PRIORITY
            </div>

            <div className="stat-value">
              {highPriorityLeads}
            </div>

            <div className="stat-description">
              Leads requiring attention
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-label">
              AVERAGE SCORE
            </div>

            <div className="stat-value">
              {averageScore}
            </div>

            <div className="stat-description">
              Opportunity strength
            </div>

          </div>


          <div className="stat-card">

            <div className="stat-label">
              GAMING SIGNALS
            </div>

            <div className="stat-value">
              {gamingSignals}
            </div>

            <div className="stat-description">
              Gaming-related leads
            </div>

          </div>

        </div>


        {/* PRIORITY LEADS */}

        <div className="section-card">

          <div className="section-header">

            <div>

              <h2>
                Priority Leads
              </h2>

              <p>
                Highest-potential opportunities
              </p>

            </div>


            <button
              className="secondary-button"
              onClick={refreshLeads}
              disabled={refreshing}
            >

              {refreshing
                ? "Refreshing..."
                : "Refresh"}

            </button>

          </div>


          <div className="table-container">

            <table>

              <thead>

                <tr>

                  <th>
                    BRAND
                  </th>

                  <th>
                    INDUSTRY
                  </th>

                  <th>
                    LEAD TYPE
                  </th>

                  <th>
                    SCORE
                  </th>

                  <th>
                    PRIORITY
                  </th>

                </tr>

              </thead>


              <tbody>

                {priorityLeads.map(
                  (lead) => (

                    <tr
                      key={lead.id}
                      className="clickable-row"
                      onClick={() =>
                        openLeadDetails(
                          lead
                        )
                      }
                    >

                      <td className="brand-name">
                        {lead.brand_name ||
                          "Unknown"}
                      </td>

                      <td>
                        {lead.industry ||
                          "Unknown"}
                      </td>

                      <td>
                        {lead.lead_type ||
                          "Unknown"}
                      </td>

                      <td>

                        <span className="score-badge">
                          {
                            lead.opportunity_score ??
                            0
                          }
                        </span>

                      </td>

                      <td>

                        <span
                          className={
                            getPriorityClass(
                              lead.priority
                            )
                          }
                        >
                          {lead.priority ||
                            "Low"}
                        </span>

                      </td>

                    </tr>

                  )
                )}


                {priorityLeads.length === 0 && (

                  <tr>

                    <td
                      colSpan="5"
                      className="empty-state"
                    >
                      No leads available.
                    </td>

                  </tr>

                )}

              </tbody>

            </table>

          </div>


          <div className="view-all-container">

            <button
              className="view-all-button"
              onClick={() =>
                goToPage("leads")
              }
            >
              View All Leads →
            </button>

          </div>

        </div>

      </div>
    );
  };


  // ==========================================
  // LEADS PAGE
  // ==========================================

  const renderLeads = () => {

    return (
      <div className="page-content">

        <div className="page-header">

          <div>

            <h1>
              All Leads
            </h1>

            <p>
              {filteredLeads.length}{" "}
              opportunities found
            </p>

          </div>


          <button
            className="secondary-button"
            onClick={refreshLeads}
            disabled={refreshing}
          >

            {refreshing
              ? "Refreshing..."
              : "Refresh Leads"}

          </button>

        </div>


        {/* SUCCESS */}

        {successMessage && (

          <div className="success-message">

            <span>
              ✓
            </span>

            {successMessage}

          </div>

        )}


        {/* ERROR */}

        {error && (

          <div className="error-message">

            <span>
              !
            </span>

            {error}

          </div>

        )}


        {/* SEARCH + FILTER */}

        <div className="filters-container">

          <div className="search-container">

            <input
              type="text"
              placeholder="Search by brand..."
              value={searchTerm}
              onChange={(event) =>
                setSearchTerm(
                  event.target.value
                )
              }
              className="search-input"
            />

          </div>


          <div className="filter-buttons">

            <button
              className={
                priorityFilter === "ALL"
                  ? "filter-button active"
                  : "filter-button"
              }
              onClick={() =>
                setPriorityFilter("ALL")
              }
            >
              All
            </button>


            <button
              className={
                priorityFilter === "HIGH"
                  ? "filter-button active"
                  : "filter-button"
              }
              onClick={() =>
                setPriorityFilter("HIGH")
              }
            >
              High
            </button>


            <button
              className={
                priorityFilter === "MEDIUM"
                  ? "filter-button active"
                  : "filter-button"
              }
              onClick={() =>
                setPriorityFilter("MEDIUM")
              }
            >
              Medium
            </button>


            <button
              className={
                priorityFilter === "LOW"
                  ? "filter-button active"
                  : "filter-button"
              }
              onClick={() =>
                setPriorityFilter("LOW")
              }
            >
              Low
            </button>

          </div>

        </div>


        {/* LEADS TABLE */}

        <div className="section-card">

          <div className="table-container">

            <table>

              <thead>

                <tr>

                  <th>
                    BRAND
                  </th>

                  <th>
                    INDUSTRY
                  </th>

                  <th>
                    LEAD TYPE
                  </th>

                  <th>
                    SCORE
                  </th>

                  <th>
                    PRIORITY
                  </th>

                  <th>
                    GAMING
                  </th>

                  <th>
                    SPONSORSHIP
                  </th>

                </tr>

              </thead>


              <tbody>

                {loading ? (

                  <tr>

                    <td
                      colSpan="7"
                      className="empty-state"
                    >
                      Loading leads...
                    </td>

                  </tr>

                ) : (

                  filteredLeads.map(
                    (lead) => (

                      <tr
                        key={lead.id}
                        className="clickable-row"
                        onClick={() =>
                          openLeadDetails(
                            lead
                          )
                        }
                      >

                        <td className="brand-name">
                          {lead.brand_name ||
                            "Unknown"}
                        </td>

                        <td>
                          {lead.industry ||
                            "Unknown"}
                        </td>

                        <td>
                          {lead.lead_type ||
                            "Unknown"}
                        </td>

                        <td>

                          <span className="score-badge">
                            {
                              lead.opportunity_score ??
                              0
                            }
                          </span>

                        </td>

                        <td>

                          <span
                            className={
                              getPriorityClass(
                                lead.priority
                              )
                            }
                          >
                            {lead.priority ||
                              "Low"}
                          </span>

                        </td>

                        <td>
                          {getSignalText(
                            lead.gaming_signal
                          )}
                        </td>

                        <td>
                          {getSignalText(
                            lead.sponsorship_signal
                          )}
                        </td>

                      </tr>

                    )
                  )

                )}


                {!loading &&
                  filteredLeads.length ===
                    0 && (

                    <tr>

                      <td
                        colSpan="7"
                        className="empty-state"
                      >
                        No leads match your
                        search or filter.
                      </td>

                    </tr>

                  )}

              </tbody>

            </table>

          </div>

        </div>

      </div>
    );
  };


  // ==========================================
  // DISCOVERY PAGE
  // ==========================================

  const renderDiscovery = () => {

    return (
      <div className="page-content">

        <div className="page-header">

          <div>

            <h1>
              Lead Discovery
            </h1>

            <p>
              Discover new gaming sponsorship
              opportunities from recent signals.
            </p>

          </div>

        </div>


        {successMessage && (

          <div className="success-message">

            <span>
              ✓
            </span>

            {successMessage}

          </div>

        )}


        {error && (

          <div className="error-message">

            <span>
              !
            </span>

            {error}

          </div>

        )}


        <div className="section-card discovery-card">

          <div className="discovery-content">

            <h2>
              VEXA AI Discovery Engine
            </h2>

            <p>
              Search recent news and identify
              potential gaming sponsorship
              opportunities using the VEXA AI
              discovery pipeline.
            </p>


            <div className="discovery-stats">

              <div>

                <strong>
                  {totalLeads}
                </strong>

                <span>
                  Current Leads
                </span>

              </div>


              <div>

                <strong>
                  {highPriorityLeads}
                </strong>

                <span>
                  High Priority
                </span>

              </div>


              <div>

                <strong>
                  {averageScore}
                </strong>

                <span>
                  Average Score
                </span>

              </div>

            </div>


            <button
              className="discovery-button large"
              onClick={runDiscovery}
              disabled={discovering}
            >

              {discovering
                ? "Running Discovery..."
                : "Run Discovery"}

            </button>


            {discovering && (

              <div className="discovery-running">

                <div className="status-spinner">
                  ⟳
                </div>

                <div>

                  <strong>
                    Discovery engine is running
                  </strong>

                  <p>
                    Searching news, analyzing
                    signals, scoring opportunities,
                    and saving leads...
                  </p>

                </div>

              </div>

            )}

          </div>

        </div>

      </div>
    );
  };


  // ==========================================
  // LEAD INTELLIGENCE DETAILS
  // ==========================================

  const renderLeadDetails = () => {

    if (!selectedLead) {
      return null;
    }


    return (
      <div
        className="modal-overlay"
        onClick={closeLeadDetails}
      >

        <div
          className="lead-details-modal"
          onClick={(event) =>
            event.stopPropagation()
          }
        >

          {/* ==================================
              MODAL HEADER
          ================================== */}

          <div className="modal-header">

            <div>

              <span className="intelligence-label">
                VEXA AI LEAD INTELLIGENCE
              </span>

              <h2>
                {selectedLead.brand_name ||
                  "Unknown"}
              </h2>

              <p>
                Sales opportunity intelligence
              </p>

            </div>


            <button
              className="close-button"
              onClick={closeLeadDetails}
            >
              ×
            </button>

          </div>


          <div className="modal-body">


            {/* ==================================
                LEAD OVERVIEW
            ================================== */}

            <div className="intelligence-section">

              <div className="intelligence-section-header">

                <h3>
                  Lead Overview
                </h3>

                <span>
                  Core opportunity information
                </span>

              </div>


              <div className="detail-grid">


                <div className="detail-item">

                  <span>
                    Brand
                  </span>

                  <strong>
                    {selectedLead.brand_name ||
                      "Unknown"}
                  </strong>

                </div>


                <div className="detail-item">

                  <span>
                    Industry
                  </span>

                  <strong>
                    {selectedLead.industry ||
                      "Unknown"}
                  </strong>

                </div>


                <div className="detail-item">

                  <span>
                    Lead Type
                  </span>

                  <strong>
                    {selectedLead.lead_type ||
                      "Unknown"}
                  </strong>

                </div>


                <div className="detail-item">

                  <span>
                    Opportunity Score
                  </span>

                  <strong className="intelligence-score">
                    {
                      selectedLead.opportunity_score ??
                      0
                    }
                  </strong>

                </div>


                <div className="detail-item">

                  <span>
                    Priority
                  </span>

                  <strong>

                    <span
                      className={
                        getPriorityClass(
                          selectedLead.priority
                        )
                      }
                    >
                      {selectedLead.priority ||
                        "Low"}
                    </span>

                  </strong>

                </div>

              </div>

            </div>


            {/* ==================================
                SIGNALS
            ================================== */}

            <div className="intelligence-section">

              <div className="intelligence-section-header">

                <h3>
                  Opportunity Signals
                </h3>

                <span>
                  Detected indicators
                </span>

              </div>


              <div className="signal-grid">


                <div
                  className={
                    selectedLead.gaming_signal
                      ? "signal-card signal-positive"
                      : "signal-card"
                  }
                >

                  <span className="signal-icon">
                    {selectedLead.gaming_signal
                      ? "✓"
                      : "—"}
                  </span>

                  <div>

                    <strong>
                      Gaming Signal
                    </strong>

                    <p>
                      {selectedLead.gaming_signal
                        ? "Gaming activity detected"
                        : "No gaming signal detected"}
                    </p>

                  </div>

                </div>


                <div
                  className={
                    selectedLead.sponsorship_signal
                      ? "signal-card signal-positive"
                      : "signal-card"
                  }
                >

                  <span className="signal-icon">
                    {selectedLead.sponsorship_signal
                      ? "✓"
                      : "—"}
                  </span>

                  <div>

                    <strong>
                      Sponsorship Signal
                    </strong>

                    <p>
                      {selectedLead.sponsorship_signal
                        ? "Sponsorship opportunity detected"
                        : "No sponsorship signal detected"}
                    </p>

                  </div>

                </div>

              </div>

            </div>


            {/* ==================================
                GAMING ACTIVITY
            ================================== */}

            {selectedLead.gaming_activity && (

              <div className="intelligence-section">

                <div className="intelligence-section-header">

                  <h3>
                    Gaming Activity
                  </h3>

                  <span>
                    Detected gaming-related activity
                  </span>

                </div>

                <div className="intelligence-text">

                  <p>
                    {selectedLead.gaming_activity}
                  </p>

                </div>

              </div>

            )}


            {/* ==================================
                SPONSORSHIP ACTIVITY
            ================================== */}

            {selectedLead.sponsorship_activity && (

              <div className="intelligence-section">

                <div className="intelligence-section-header">

                  <h3>
                    Sponsorship Activity
                  </h3>

                  <span>
                    Commercial partnership signal
                  </span>

                </div>

                <div className="intelligence-text">

                  <p>
                    {
                      selectedLead.sponsorship_activity
                    }
                  </p>

                </div>

              </div>

            )}


            {/* ==================================
                OPPORTUNITY
            ================================== */}

            {selectedLead.opportunity && (

              <div className="intelligence-section">

                <div className="intelligence-section-header">

                  <h3>
                    Opportunity
                  </h3>

                  <span>
                    Potential sales opportunity
                  </span>

                </div>

                <div className="opportunity-box">

                  <p>
                    {selectedLead.opportunity}
                  </p>

                </div>

              </div>

            )}


            {/* ==================================
                AI REASONING
            ================================== */}

            {selectedLead.reasoning && (

              <div className="intelligence-section">

                <div className="intelligence-section-header">

                  <h3>
                    AI Reasoning
                  </h3>

                  <span>
                    Why VEXA identified this lead
                  </span>

                </div>

                <div className="reasoning-box">

                  <p>
                    {selectedLead.reasoning}
                  </p>

                </div>

              </div>

            )}


            {/* ==================================
                EVIDENCE
            ================================== */}

            {selectedLead.title && (

              <div className="intelligence-section">

                <div className="intelligence-section-header">

                  <h3>
                    Evidence
                  </h3>

                  <span>
                    Source signal used for discovery
                  </span>

                </div>

                <div className="evidence-box">

                  <p>
                    {selectedLead.title}
                  </p>

                </div>

              </div>

            )}


            {/* ==================================
                SOURCE
            ================================== */}

            {selectedLead.source_url && (

              <div className="intelligence-section">

                <div className="intelligence-section-header">

                  <h3>
                    Source Article
                  </h3>

                  <span>
                    Original evidence
                  </span>

                </div>

                <a
                  className="source-link"
                  href={
                    selectedLead.source_url
                  }
                  target="_blank"
                  rel="noreferrer"
                >
                  View Source Article →
                </a>

              </div>

            )}

          </div>

        </div>

      </div>
    );
  };


  // ==========================================
  // MAIN APPLICATION
  // ==========================================

  return (
    <div className="app">

      {/* ======================================
          SIDEBAR
      ====================================== */}

      <aside className="sidebar">

        <div className="sidebar-brand">

          <h1>
            VEXA
          </h1>

          <p>
            Sales Intelligence
          </p>

        </div>


        <nav className="sidebar-nav">

          <button
            className={
              currentPage === "dashboard"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              goToPage("dashboard")
            }
          >
            Dashboard
          </button>


          <button
            className={
              currentPage === "leads"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              goToPage("leads")
            }
          >
            Leads
          </button>


          <button
            className={
              currentPage === "discovery"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              goToPage("discovery")
            }
          >
            Discovery
          </button>

        </nav>


        <div className="sidebar-footer">

          Prototype v1.0

        </div>

      </aside>


      {/* ======================================
          MAIN CONTENT
      ====================================== */}

      <main className="main-content">

        {currentPage === "dashboard" &&
          renderDashboard()}

        {currentPage === "leads" &&
          renderLeads()}

        {currentPage === "discovery" &&
          renderDiscovery()}

      </main>


      {/* ======================================
          LEAD INTELLIGENCE MODAL
      ====================================== */}

      {selectedLead &&
        renderLeadDetails()}

    </div>
  );
}

export default App;