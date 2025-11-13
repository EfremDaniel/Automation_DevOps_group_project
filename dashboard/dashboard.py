import streamlit as st
from connect_data_warehouse import query_job_listings
import altair as alt
import pandas as pd

if "economics_df" not in st.session_state:
    st.session_state["economics_df"] = query_job_listings(
        "SELECT * FROM marts.mart_economics"
    )
if "data_df" not in st.session_state:
    st.session_state["data_df"] = query_job_listings("SELECT * FROM marts.mart_it")
if "construction_df" not in st.session_state:
    st.session_state["construction_df"] = query_job_listings(
        "SELECT * FROM marts.mart_construction"
    )

st.set_page_config(layout="wide")
page1 = st.sidebar.radio("Meny", ["Start", "Annonser"])
page2 = st.sidebar.radio(
    "Data", ["Bygg och anläggning", "Data/IT", "Administration, ekonomi, juridik"]
)


# Order dataframe by vacancies
@st.cache_data
def order_by_vacancies(df, col):
    df = df.sort_values("VACANCIES", ascending=False)
    df[col] = pd.Categorical(df[col], categories=df[col], ordered=True)
    return df


@st.cache_data
def filter_df(df, col_group, col):
    df_filtered = df.groupby(col_group, as_index=False)[col].sum()
    return df_filtered


def layout_graphs(df, name):
    st.title(f"{name}-annonser")
    st.write("En dashboard som visar annonser från arbetsförmedlingens API. ")

    cols = st.columns(2)

    with cols[0]:
        st.metric(label="Total vacancies", value=int(df["VACANCIES"].sum()))

    with cols[1]:
        st.metric(label="Total ads", value=len(df))

    df_employer = filter_df(df, "EMPLOYER_NAME", "VACANCIES")
    df_occupation = filter_df(df, "OCCUPATION", "VACANCIES")
    df_region = filter_df(df, "WORKPLACE_REGION", "VACANCIES")
    df_duration = filter_df(df, "DURATION", "VACANCIES")

    df_employer = order_by_vacancies(df_employer, "EMPLOYER_NAME")
    df_occupation = order_by_vacancies(df_occupation, "OCCUPATION")
    df_region = order_by_vacancies(df_region, "WORKPLACE_REGION")
    df_duration = order_by_vacancies(df_duration, "DURATION")

    cols = st.columns(2)

    with cols[0]:
        st.write("### Top 10 Employers by Vacancies")
        st.write(
            alt.Chart(df_employer.head(10))
            .mark_bar()
            .encode(
                x=alt.X("EMPLOYER_NAME", title="Employer"),
                y=alt.Y("VACANCIES", title="Vacancies"),
                color=alt.Color("EMPLOYER_NAME:N", legend=None),
                tooltip=["EMPLOYER_NAME", "VACANCIES"],
            )
        )

    with cols[1]:
        st.write("### Top 10 Occupations by Vacancies")
        st.write(
            alt.Chart(df_occupation.head(10))
            .mark_bar()
            .encode(
                x=alt.X("OCCUPATION", title="Occupation"),
                y=alt.Y("VACANCIES", title="Vacancies"),
                color=alt.Color("OCCUPATION:N", legend=None),
                tooltip=["OCCUPATION", "VACANCIES"],
            )
        )

    cols = st.columns(2)

    with cols[0]:
        st.write("### Top 10 Regions by Vacancies")
        st.write(
            alt.Chart(df_region.head(10))
            .mark_bar()
            .encode(
                x=alt.X("WORKPLACE_REGION", title="Region"),
                y=alt.Y("VACANCIES", title="Vacancies"),
                color=alt.Color("WORKPLACE_REGION:N", legend=None),
                tooltip=["WORKPLACE_REGION", "VACANCIES"],
            )
        )

    with cols[1]:
        st.write("### Duration of employment by Vacancies")
        st.write(
            alt.Chart(df_duration.head(10))
            .mark_bar()
            .encode(
                x=alt.X("DURATION", title="Duration"),
                y=alt.Y("VACANCIES", title="Vacancies"),
                color=alt.Color("DURATION:N", legend=None),
                tooltip=["DURATION", "VACANCIES"],
            )
        )


def layout_ads(df: pd.DataFrame):
    cols = st.columns(4)
    with cols[0]:
        st.selectbox("Select region:", df["WORKPLACE_REGION"].unique())
    with cols[1]:
        st.selectbox(
            "Select occupation:",
            df.query("WORKPLACE_REGION == @select_region")["OCCUPATION"].unique(),
        )
    with cols[2]:
        st.selectbox(
            "Select company:",
            df.query(
                "WORKPLACE_REGION == @select_region & OCCUPATION == @select_occupation"
            )["EMPLOYER_NAME"].unique(),
        )
    with cols[3]:
        st.selectbox(
            "Select headline:",
            df.query(
                "WORKPLACE_REGION == @select_region & OCCUPATION == @select_occupation & EMPLOYER_NAME == @select_company"  # noqa: E501
            )["HEADLINE"],
        )

    st.markdown("## Job listings data")
    sel = df.query(
        "WORKPLACE_REGION == @select_region & OCCUPATION == @select_occupation & EMPLOYER_NAME == @select_company & HEADLINE == @select_headline"  # noqa: E501
    )

    row = sel.iloc[0]
    st.markdown(row["DESCRIPTION_HTML"], unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Vacancies </h4>", unsafe_allow_html=True
        )
        st.markdown(f"{row['VACANCIES']}")

    with cols[1]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Application deadline </h4>",
            unsafe_allow_html=True,
        )
        st.markdown(f"{row['APPLICATION_DEADLINE']}")

    with cols[2]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Duration </h4>", unsafe_allow_html=True
        )
        st.markdown(f"{row['DURATION']}")

    with cols[3]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Employment type </h4>",
            unsafe_allow_html=True,
        )
        st.markdown(f"{row['EMPLOYMENT_TYPE']}")

    cols = st.columns(4)

    with cols[0]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Salary type </h4>", unsafe_allow_html=True
        )
        st.markdown(f"{row['SALARY_TYPE']}")

    with cols[1]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Job ID </h4>", unsafe_allow_html=True
        )
        st.markdown(f"{row['JOB_DESCRIPTION_ID']}")

    with cols[2]:
        st.markdown(
            "<h4 style= 'color:steelblue'> Occupation group </h4>",
            unsafe_allow_html=True,
        )
        st.markdown(f"{row['OCCUPATION_GROUP']}")


if page2 == "Bygg och anläggning":
    dashboard_df = st.session_state["construction_df"]
    name = "Bygg och anläggning"
elif page2 == "Data/IT":
    dashboard_df = st.session_state["data_df"]
    name = "Data/IT"
elif page2 == "Administration, ekonomi, juridik":
    dashboard_df = st.session_state["economics_df"]
    name = "Administration, ekonomi, juridik"

if page1 == "Start":
    layout_graphs(dashboard_df, name)
elif page1 == "Annonser":
    layout_ads(dashboard_df)
