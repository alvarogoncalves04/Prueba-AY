import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

df = pd.read_csv('pitcheo.csv', encoding = 'latin-1', sep = ';')

df