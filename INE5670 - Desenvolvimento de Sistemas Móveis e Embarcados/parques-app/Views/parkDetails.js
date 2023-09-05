import * as React from 'react';
import {
  Text,
  View,
  Linking,
  Platform,
  Image,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { SocialIcon } from 'react-native-elements';
import { WebView } from 'react-native-webview';
import {BACKGROUND_COLOR, HEADER_COLOR} from '../config.js';
import styles from '../styles/parksDetailsStyles';
import stylesButton from '../styles/buttonStyle';


export default class ParkDetailsScreen extends React.Component {
  static navigationOptions = {
    title: 'Detalhes',
    headerStyle: {
      backgroundColor: HEADER_COLOR,
      borderBottomColor: HEADER_COLOR,
      borderBottomWidth: 3,
        shadowOffset: {
          width: 0,
          height: 3,
        },
        shadowOpacity: 0.3,
        shadowRadius: 4.65,
        elevation: 6,
        },
    headerTitleStyle: {
      fontSize: 18,
      color: 'white',
    },
    headerTintColor: 'white',
  };

  constructor(props) {
    super(props);
    let park = props.navigation.getParam('park');
    this.state = {
      name: park.name,
      street: park.address.street,
      city: park.address.city,
      uf: park.address.UF,
      zipcode:  park.address.zipcode,
      lat: park.address.geo.lat,
      lng: park.address.geo.lng,
      images: park.images,
      video: park.video,
      website: park.contact.website,
      instagram: park.social_midia.instagram,
      facebook: park.social_midia.facebook,
      ticket_price: park.ticket_price,
      buy_tickets: park.buy_tickets,
      phone: park.contact.phone,
      email: park.contact.email,
      logo: park.logo

    };
  }

  render() {
    const { navigate } = this.props.navigation;
    const { name, street, city, uf, zipcode, lat, lng, images, video, website, instagram, facebook, ticket_price, buy_tickets, phone, email, logo} = this.state;

    const mapUrl = Platform.select({
      ios: `maps:${lat},${lng}?q=${lat},${lng}`,
      android: `geo:${lat},${lng}?q=${lat},${lng}`,
    });

    return (
      <ScrollView style={{backgroundColor: BACKGROUND_COLOR}}>
        <View style={styles.container}>
          <Image style={styles.logo} source={{uri: logo}} />
          <Text style={styles.name}>{name}</Text>
          <Text style={styles.address}>{`${street} ${city} - ${uf}, ${zipcode}`}</Text>
        </View>
        <View style={stylesButton.buttonContainer}> 
          <TouchableOpacity style={stylesButton.button} onPress={ () =>  Linking.openURL(mapUrl)}>
            <Text style={stylesButton.buttonText}>Ver mapa</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.imageContainer}> 
          {images.map((image) => (
            <Image style={styles.image} source={{ uri: image }} />
          ))}
        </View> 
        <View style={styles.imageContainer}>
          <WebView
            style={styles.image}
            mediaPlaybackRequiresUserAction={true}
            scalesPageToFit={true} 
            javaScriptEnabled={true}
            domStorageEnabled={true}
            source={{uri: video}}
          />
        </View>
        <View style={stylesButton.buttonContainer}> 
          <TouchableOpacity style={stylesButton.button} onPress={ () =>  Linking.openURL(buy_tickets)}>
            <Text style={stylesButton.buttonText}>{`Ingressos ${ticket_price}`}</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.contactContainer}>
          <Text style={styles.name}> Contatos </Text>
          <View style={styles.socialsContainer}> 
            <TouchableOpacity onPress={ () => Linking.openURL(facebook)}>
            <SocialIcon type='facebook' />
            </TouchableOpacity>
            <TouchableOpacity onPress={ () => Linking.openURL(instagram)}>
              <SocialIcon type='instagram' />
            </TouchableOpacity>
          </View>
          <TouchableOpacity onPress={ () => Linking.openURL(`tel://${phone}`)}>
            <Text style={styles.contactDetails}>{phone}</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={ () => Linking.openURL(website)}>
            <Text style={styles.contactDetails}>{`${website}`}</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={ () => Linking.openURL(`mailto:${email}`)}>
            <Text style={styles.contactDetails}>{email}</Text>
          </TouchableOpacity>
        </View>
        <View style={stylesButton.buttonContainer}>
          <TouchableOpacity style={stylesButton.button} onPress={() => navigate('ParksList')} activeOpacity={0.6}>
             <Text style={stylesButton.buttonText}>Voltar</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  }
}
