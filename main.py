import streamlit as st
import pandas as pd
import io
import json
from datetime import datetime
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="PR Pulse - Smart Media Query Explorer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        display: flex; align-items: center; gap: 10px;
        padding-bottom: 20px; border-bottom: 2px solid #e2e8f0;
        margin-bottom: 30px;
    }
    .stat-card {
        background: white; border-radius: 12px; padding: 20px;
        border: 1px solid #e2e8f0; text-align: center;
    }
    .match-card {
        background: #f8fafc; border-radius: 8px; padding: 15px;
        border: 1px solid #e2e8f0; margin: 10px 0;
    }
    .query-card {
        background: white; border-radius: 12px; padding: 20px;
        border: 1px solid #e2e8f0; margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "all_queries" not in st.session_state:
    st.session_state.all_queries = []
if "filtered_queries" not in st.session_state:
    st.session_state.filtered_queries = []
if "expert_bio" not in st.session_state:
    st.session_state.expert_bio = ""
if "selected_query_idx" not in st.session_state:
    st.session_state.selected_query_idx = None

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("⚡", unsafe_allow_html=True)
with col2:
    st.markdown("### PR Pulse - Smart Media Query Explorer & Pitching Assistant")
    st.markdown("*Powered by Gemini AI | Media Query Management for PR Professionals*")

st.divider()

# Sidebar: Configuration & Expert Profile
with st.sidebar:
    st.header("🎯 Expert Pitch Profile")
    
    expert_bio = st.text_area(
        "Your Professional Background",
        value=st.session_state.expert_bio,
        height=120,
        placeholder="e.g., Dr. Taylor, 10+ years in Sleep Science & Neurobiology, founder of RestWell app...",
        help="Provide details about you or your expertise. Gemini will use this to find perfect matches and auto-pitch."
    )
    
    if st.button("💾 Save Profile", use_container_width=True, key="save_bio"):
        st.session_state.expert_bio = expert_bio
        st.success("Expert profile saved!")
    
    st.divider()
    
    # Gemini API Key Configuration
    st.subheader("🔑 Gemini API Setup")
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        help="Get it from https://ai.google.dev/",
        key="gemini_key_input"
    )
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("✓ Gemini API configured")
    
    st.divider()
    
    # Filters
    st.subheader("🔍 Search & Filter")
    
    if st.session_state.all_queries:
        categories = sorted(set(q.get("CATEGORY", "General") for q in st.session_state.all_queries if q.get("CATEGORY")))
        selected_category = st.selectbox(
            "Filter by Category",
            ["All Categories"] + categories,
            key="category_filter"
        )
        
        min_da = st.slider(
            "Minimum Domain Authority (DA)",
            0, 100, 0,
            help="Filter by Domain Authority score",
            key="da_filter"
        )
        
        journalist_search = st.text_input(
            "Search by Journalist Name",
            key="journalist_filter",
            placeholder="e.g., Innes Wong"
        )
        
        outlet_search = st.text_input(
            "Search by Media Outlet",
            key="outlet_filter",
            placeholder="e.g., Forbes, TechCrunch"
        )
        
        exclude_past = st.checkbox(
            "Exclude passed deadlines",
            key="exclude_past_filter"
        )

# Main Content Area
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "⚙️ Import Data", "🤖 AI Tools"])

with tab2:
    st.header("Import Media Queries")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV file with media queries",
            type="csv",
            help="Supported columns: SUMMARY, CATEGORY, QUERY, QUESTIONS, MEDIA OUTLET, DA, NAME, EMAIL"
        )
    
    with col2:
        if st.button("📋 Load Sample Data", use_container_width=True):
            sample_data = [
                {
                    "SUMMARY": "How Fintech is Changing Consumer Habits in Financial Management",
                    "CATEGORY": "Business and Finance",
                    "NAME": "Innes Wong",
                    "EMAIL": "inneswong8@gmail.com",
                    "MEDIA_OUTLET": "Techcabal",
                    "QUERY": "Fintech is revolutionizing consumer financial management...",
                    "QUESTIONS": "What consumer behaviors have changed most? Key adoption bottlenecks?",
                    "DA": 82
                },
                {
                    "SUMMARY": "Puerto Rican Rum History and Distillery Tastings",
                    "CATEGORY": "Lifestyle",
                    "NAME": "Stephanie Aviles",
                    "EMAIL": "stephanie.marie.aviles@gmail.com",
                    "MEDIA_OUTLET": "Mitu",
                    "QUERY": "Writing about Puerto Rican rum and seeking sources...",
                    "QUESTIONS": "What sets PR rum apart? Which distilleries push boundaries?",
                    "DA": 71
                },
                {
                    "SUMMARY": "Tech Companies & Burnout Prevention Tactics",
                    "CATEGORY": "High Tech",
                    "NAME": "Marcus Vance",
                    "EMAIL": "marcus@wiredtech.io",
                    "MEDIA_OUTLET": "Wired Tech",
                    "QUERY": "Looking for experts on preventing engineering burnout...",
                    "QUESTIONS": "What metrics indicate burnout? Which tools help?",
                    "DA": 58
                }
            ]
            st.session_state.all_queries = sample_data
            st.session_state.filtered_queries = sample_data
            st.success(f"Loaded {len(sample_data)} sample queries!")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Normalize column names
            df.columns = df.columns.str.strip().str.upper()
            
            # Required columns mapping
            column_mapping = {
                "SUMMARY": "SUMMARY",
                "TITLE": "SUMMARY",
                "CATEGORY": "CATEGORY",
                "TOPIC": "CATEGORY",
                "NAME": "NAME",
                "REPORTER": "NAME",
                "JOURNALIST": "NAME",
                "EMAIL": "EMAIL",
                "MEDIA OUTLET": "MEDIA_OUTLET",
                "OUTLET": "MEDIA_OUTLET",
                "SOURCE": "MEDIA_OUTLET",
                "QUERY": "QUERY",
                "DESCRIPTION": "QUERY",
                "QUESTIONS": "QUESTIONS",
                "DA": "DA",
                "DOMAIN AUTHORITY": "DA"
            }
            
            # Rename columns
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df[new_col] = df[old_col]
            
            # Ensure required columns
            for col in ["SUMMARY", "CATEGORY", "QUERY", "DA", "MEDIA_OUTLET", "NAME"]:
                if col not in df.columns:
                    df[col] = ""
            
            # Convert to records
            records = df[["SUMMARY", "CATEGORY", "QUERY", "QUESTIONS", "MEDIA_OUTLET", "NAME", "EMAIL", "DA"]].to_dict("records")
            
            # Handle append vs overwrite
            if st.session_state.all_queries:
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Append to existing", use_container_width=True):
                        st.session_state.all_queries.extend(records)
                        st.session_state.filtered_queries = st.session_state.all_queries
                        st.success(f"Appended {len(records)} records!")
                with col2:
                    if st.button("Overwrite existing", use_container_width=True):
                        st.session_state.all_queries = records
                        st.session_state.filtered_queries = records
                        st.success(f"Loaded {len(records)} records (previous cleared)")
            else:
                st.session_state.all_queries = records
                st.session_state.filtered_queries = records
                st.success(f"Successfully loaded {len(records)} media queries!")
            
            st.dataframe(df.head(10), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error processing CSV: {str(e)}")

with tab1:
    if not st.session_state.all_queries:
        st.info("👆 Go to the 'Import Data' tab to upload or load sample media queries")
    else:
        # Apply Filters
        filtered = st.session_state.all_queries.copy()
        
        # Category filter
        if "category_filter" in st.session_state and st.session_state.category_filter != "All Categories":
            filtered = [q for q in filtered if q.get("CATEGORY") == st.session_state.category_filter]
        
        # DA filter
        if "da_filter" in st.session_state:
            min_da = st.session_state.da_filter
            filtered = [q for q in filtered if int(q.get("DA", 0)) >= min_da]
        
        # Journalist filter
        if "journalist_filter" in st.session_state and st.session_state.journalist_filter:
            term = st.session_state.journalist_filter.lower()
            filtered = [q for q in filtered if term in q.get("NAME", "").lower()]
        
        # Outlet filter
        if "outlet_filter" in st.session_state and st.session_state.outlet_filter:
            term = st.session_state.outlet_filter.lower()
            filtered = [q for q in filtered if term in q.get("MEDIA_OUTLET", "").lower()]
        
        # Exclude past deadlines
        if "exclude_past_filter" in st.session_state and st.session_state.exclude_past_filter:
            today = datetime.now().date()
            filtered = [q for q in filtered if not q.get("DEADLINE_DATE") or datetime.strptime(q.get("DEADLINE_DATE"), "%Y-%m-%d").date() >= today]
        
        st.session_state.filtered_queries = filtered
        
        # Analytics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Matching Queries", len(filtered))
        
        with col2:
            avg_da = sum(int(q.get("DA", 0)) for q in filtered) / len(filtered) if filtered else 0
            st.metric("Average DA", f"{int(avg_da)}")
        
        with col3:
            if filtered:
                top_cat = max(set(q.get("CATEGORY", "General") for q in filtered), 
                            key=lambda x: sum(1 for q in filtered if q.get("CATEGORY") == x))
                st.metric("Top Category", top_cat)
        
        with col4:
            today = datetime.now().date()
            active = sum(1 for q in filtered if not q.get("DEADLINE_DATE") or datetime.strptime(q.get("DEADLINE_DATE"), "%Y-%m-%d").date() >= today)
            st.metric("Active Today", active)
        
        st.divider()
        
        # Display Results
        st.subheader(f"Results ({len(filtered)} found)")
        
        # Download CSV
        if filtered:
            csv = pd.DataFrame(filtered).to_csv(index=False)
            st.download_button(
                "📥 Download Results as CSV",
                csv,
                "pr_pulse_search_results.csv",
                "text/csv",
                use_container_width=True
            )
            st.divider()
        
        # Query Cards
        for idx, query in enumerate(filtered):
            with st.expander(f"**{query.get('MEDIA_OUTLET', 'Unknown')}** - {query.get('SUMMARY', 'No Title')}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**Category:** {query.get('CATEGORY', 'General')}")
                with col2:
                    st.write(f"**DA:** {query.get('DA', 'N/A')}")
                with col3:
                    st.write(f"**Reporter:** {query.get('NAME', 'N/A')}")
                with col4:
                    st.write(f"**Email:** {query.get('EMAIL', 'Direct Only')}")
                
                st.write(f"**Query:** {query.get('QUERY', 'No description')}")
                
                if query.get('QUESTIONS'):
                    st.write(f"**Questions:** {query.get('QUESTIONS')}")
                
                if st.button(f"🤖 Draft AI Pitch", key=f"pitch_{idx}"):
                    st.session_state.selected_query_idx = idx

with tab3:
    st.header("🤖 AI-Powered Tools")
    
    if not st.session_state.expert_bio:
        st.warning("Please save your Expert Profile in the sidebar first")
    elif not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar")
    else:
        tool_choice = st.radio("Select Tool", ["Smart Search Expansion", "AI Matchmaker"], horizontal=True)
        
        if tool_choice == "Smart Search Expansion":
            st.subheader("Smart Search Brain")
            search_query = st.text_input("Enter a concept or product to search for", placeholder="e.g., Sleep tech, AI health monitoring")
            
            if st.button("🔍 Expand Search with AI"):
                with st.spinner("AI is analyzing search concepts..."):
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        
                        prompt = f"""
                        Parse this user's vague product query: "{search_query}"
                        Generate expanded search terms and related categories for media queries.
                        Return JSON with:
                        {{
                            "searchTerms": ["term1", "term2", ...],
                            "suggestedCategories": ["cat1", "cat2", ...],
                            "analysis": "Why these keywords are relevant"
                        }}
                        """
                        
                        response = model.generate_content(prompt)
                        
                        # Parse response
                        try:
                            result = json.loads(response.text)
                            
                            st.success("AI Search Expansion Complete!")
                            st.markdown(f"**Analysis:** {result.get('analysis', 'N/A')}")
                            
                            st.write("**Search Terms Found:**")
                            terms = result.get('searchTerms', [])
                            filtered = [q for q in st.session_state.all_queries if any(
                                term.lower() in (q.get('SUMMARY', '') + q.get('QUERY', '') + q.get('QUESTIONS', '')).lower()
                                for term in terms
                            )]
                            
                            st.metric(f"Matching Queries", len(filtered))
                            
                            for term in terms:
                                st.write(f"- {term}")
                            
                            if filtered:
                                st.divider()
                                st.write(f"**Found {len(filtered)} Matching Opportunities**")
                                for q in filtered[:5]:
                                    st.write(f"- {q.get('MEDIA_OUTLET')} | {q.get('SUMMARY')}")
                        
                        except json.JSONDecodeError:
                            st.error("Could not parse AI response")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # AI Matchmaker
            st.subheader("AI Matchmaker - Find Your Perfect Targets")
            
            if st.button("🎯 Analyze Top 10 Matches"):
                if not st.session_state.filtered_queries:
                    st.warning("No queries match current filters")
                else:
                    with st.spinner("Gemini is analyzing targets..."):
                        try:
                            model = genai.GenerativeModel("gemini-2.5-flash")
                            
                            batch = st.session_state.filtered_queries[:10]
                            
                            prompt = f"""
                            EXPERT: {st.session_state.expert_bio}
                            
                            MEDIA QUERIES:
                            {json.dumps([{{'outlet': q.get('MEDIA_OUTLET'), 'summary': q.get('SUMMARY'), 'query': q.get('QUERY')}} for q in batch], indent=2)}
                            
                            Score each match 1-100 based on fit with the expert's background. Return JSON:
                            {{
                                "matches": [
                                    {{"index": 0, "score": 95, "logic": "..."}}
                                ]
                            }}
                            """
                            
                            response = model.generate_content(prompt)
                            
                            try:
                                matches = json.loads(response.text)
                                matches['matches'].sort(key=lambda x: x['score'], reverse=True)
                                
                                st.success("Analysis Complete!")
                                
                                for match in matches['matches']:
                                    idx = match['index']
                                    q = batch[idx]
                                    
                                    col1, col2 = st.columns([4, 1])
                                    with col1:
                                        st.write(f"**{q.get('MEDIA_OUTLET')}** | {q.get('SUMMARY')}")
                                        st.caption(f"__{match['logic']}__")
                                    with col2:
                                        st.metric("Fit Score", f"{match['score']}%")
                                    
                                    st.divider()
                            
                            except json.JSONDecodeError:
                                st.error("Could not parse AI response")
                        
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

# Pitch Generator Sidebar
if st.session_state.selected_query_idx is not None:
    query = st.session_state.filtered_queries[st.session_state.selected_query_idx]
    
    st.sidebar.divider()
    st.sidebar.header("✍️ Draft PR Pitch")
    
    if not api_key:
        st.sidebar.warning("Need Gemini API key to generate pitches")
    else:
        if st.sidebar.button("Generate Pitch with Gemini"):
            with st.spinner("Generating pitch..."):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    
                    prompt = f"""
                    Write a professional, targeted PR response (150-250 words) for a journalist inquiry.
                    
                    EXPERT: {st.session_state.expert_bio}
                    OUTLET: {query.get('MEDIA_OUTLET')}
                    QUERY: {query.get('QUERY')}
                    QUESTIONS: {query.get('QUESTIONS')}
                    
                    Include: expert intro, direct answers to questions, professional tone.
                    Format with subject line and clear structure.
                    """
                    
                    response = model.generate_content(prompt)
                    
                    st.sidebar.success("Pitch Generated!")
                    st.sidebar.text_area("Your PR Pitch", response.text, height=300)
                    
                    # Email link
                    email = query.get('EMAIL')
                    if email:
                        mailto_link = f"mailto:{email}?subject=Expert%20Source%20Available&body={response.text.replace(chr(10), '%0A')}"
                        st.sidebar.markdown(f"[📧 Open in Email](javascript:void(0);)")
                    
                    # Copy to clipboard
                    st.sidebar.write("_Copy the pitch text above to use elsewhere_")
                
                except Exception as e:
                    st.sidebar.error(f"Error: {str(e)}")
        
        if st.sidebar.button("Close"):
            st.session_state.selected_query_idx = None
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; margin-top: 20px;">
    <p>PR Pulse © 2026 | Powered by Gemini AI | Runs securely in your browser</p>
</div>
""", unsafe_allow_html=True)
