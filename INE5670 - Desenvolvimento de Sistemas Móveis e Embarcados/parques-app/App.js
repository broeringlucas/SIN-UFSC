 import * as React from 'react';
import { createAppContainer } from 'react-navigation';
import { createStackNavigator } from 'react-navigation-stack';
import HomeScreen from './Views/Home';
import ParksListScreen from './Views/parksList'
import ParkDetailsScreen from './Views/parkDetails'
import FavoriteParksScreen from './Views/favoriteParks.js'

const MainNavigator = createStackNavigator({
  Home: { screen: HomeScreen },
  ParksList : {screen: ParksListScreen},
  ParkDetails: {screen: ParkDetailsScreen},
  FavoriteParks: {screen: FavoriteParksScreen},
});

const App = createAppContainer(MainNavigator);
export default App;
