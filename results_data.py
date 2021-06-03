import pandas as pd
results_raw_data = {'Date': ['2021-03-31', '2021-04-07', '2021-04-14', '2021-04-21', '2021-04-28', '2021-05-05', '2021-05-12', '2021-05-19', '2021-05-26', '2021-06-02'], 'Team A Result?': ['14', '7', '16', '10', '18', '8', '8', '15', '14', '14'], 'Team B Result?': ['26', '8', '21', '14', '13', '6', '11', '22', '14', '11'], 'Team A Total': ['345', '334', '356', '356', '346', '352', '372', '383', '393', '370'], 'Team B Total': ['354', '344', '362', '370', '356', '340', '369', '382', '392', '374'], 'Team A Player 1': ['Cal', 'Bernard', 'Cal', 'Cal', 'Bernard', 'Bernard', 'Bernard', 'Cal', 'Pete', 'Cal'], 'Team A Player 2': ['Ferdi', 'Darren', 'Ferdi', 'Dida', 'Kevin', 'Cal', 'Conor', 'Ferdi', 'Cal', 'Dida'], 'Team A Player 3': ['James', 'Pete', 'Pete', 'James', 'Phil', 'Kevin', 'Ferdi', 'Pete', 'Joe', 'Ferdi'], 'Team A Player 4': ['Joe', 'Simon', 'Richard', 'Pete', 'Rik', 'Pete', 'Rik', 'Phil', 'Ferdi', 'Joe'], 'Team A Player 5': ['Kevin', 'Tom', 'Rik', 'Simon', 'Tom', 'Rik', 'Simon', 'Rik', 'Bernard', 'Matt'], 'Team B Player 1': ['Darren', 'Cal', 'Bernard', 'Bernard', 'Cal', 'Ferdi', 'Cal', 'Dida', 'Dida', 'Bernard'], 'Team B Player 2': ['Dida', 'Dida', 'Darren', 'Conor', 'Ferdi', 'James', 'Chris', 'Joe', 'Darren', 'Darren'], 'Team B Player 3': ['Pete', 'Ferdi', 'Dida', 'Ferdi', 'Pete', 'Joe', 'Dida', 'Matt', 'Chris', 'James'], 'Team B Player 4': ['Rik', 'Kevin', 'Joe', 'Gavin', 'Richard', 'Keith', 'Kevin', 'Richard', 'Conor', 'Pete'], 'Team B Player 5': ['Simon', 'Rik', 'Simon', 'Rik', 'Simon', 'Simon', 'Pete', 'Simon', 'Simon', 'Simon']}
results_df = pd.DataFrame(results_raw_data, columns = ['Date', 'Team A Result?', 'Team B Result?', 'Team A Total', 'Team B Total', 'Team A Player 1', 'Team A Player 2', 'Team A Player 3', 'Team A Player 4', 'Team A Player 5', 'Team B Player 1', 'Team B Player 2', 'Team B Player 3', 'Team B Player 4', 'Team B Player 5'])