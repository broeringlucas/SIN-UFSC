package org.lucas.broering;

import org.apache.commons.codec.binary.Base32;
import org.apache.commons.codec.binary.Hex;

import javax.crypto.Cipher;
import javax.crypto.Mac;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.net.URL;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.Scanner;

public class Client {
    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        Server servidor = new Server();
        System.out.println("1 - Cadastrar novo usuário\n2 - Login e enviar mensagem");
        int opcao = scanner.nextInt();
        scanner.nextLine();

        if (opcao == 1) {
            System.out.print("Nome: ");
            String nome = scanner.nextLine();
            System.out.print("Celular: ");
            String celular = scanner.nextLine();
            System.out.print("Senha: ");
            String senha = scanner.nextLine();

            String salt = gerarSalt();
            String senhaHash = hashSenhaComScrypt(senha, salt);
            String totpSecret = gerarSecretTotp();
            String pais = obterPaisDoIP();

            User usuario = new User(nome, celular, pais, senhaHash, salt, totpSecret);
            if (servidor.cadastrarUsuario(usuario)) {
                System.out.println("Usuário cadastrado com sucesso!");
                System.out.println("TOTP Secret: " + totpSecret);
            } else {
                System.out.println("Usuário já existe.");
            }
        } else if (opcao == 2) {
            System.out.print("Nome: ");
            String nome = scanner.nextLine();
            System.out.print("Senha: ");
            String senha = scanner.nextLine();

            User u = servidor.buscarUsuario(nome);
            if (u == null) {
                System.out.println("Usuário não encontrado.");
                return;
            }

            String paisAtual = obterPaisDoIP();
            if (!u.getPais().equalsIgnoreCase(paisAtual)) {
                System.out.println("Login recusado: país de origem diferente do cadastro.");
                System.out.println("País cadastrado: " + u.getPais() + ", País atual: " + paisAtual);
                return;
            }

            String senhaTentativaHash = hashSenhaComScrypt(senha, u.getSalt());
            if (!senhaTentativaHash.equals(u.getSenhaHash())) {
                System.out.println("Senha incorreta.");
                return;
            }

            System.out.println("[DEBUG] TOTP atual: " + gerarTotpComTempo(u.getTotpSecret(), System.currentTimeMillis() / 1000 / 30));
            System.out.print("Digite o código TOTP: ");
            String totpCode = scanner.nextLine();

            if (!validarTotp(u.getTotpSecret(), totpCode)) {
                System.out.println("Código TOTP inválido ou expirado.");
                return;
            }

            SecretKey chave = derivarChave(totpCode);
            byte[] iv = new byte[12];
            new SecureRandom().nextBytes(iv);

            System.out.print("Mensagem a ser enviada: ");
            String mensagem = scanner.nextLine();
            byte[] mensagemCifrada = cifrarMensagem(mensagem, chave, iv);

            System.out.println("Mensagem cifrada enviada.");
            try {
                String decifrada = servidor.decifrarMensagem(mensagemCifrada, iv, chave);
                System.out.println("Mensagem recebida no servidor: " + decifrada);
            } catch (Exception e) {
                System.out.println("Erro ao decifrar: " + e.getMessage());
            }
        }
    }

    private static String gerarSalt() {
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);
        return Hex.encodeHexString(salt);
    }

    private static String hashSenhaComScrypt(String senha, String salt) {
        try {
            byte[] saltBytes = Hex.decodeHex(salt.toCharArray());
            PBEKeySpec spec = new PBEKeySpec(senha.toCharArray(), saltBytes, 16384, 256);
            SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
            byte[] hash = skf.generateSecret(spec).getEncoded();
            return Hex.encodeHexString(hash);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao gerar hash da senha", e);
        }
    }

    private static String gerarSecretTotp() {
        byte[] buffer = new byte[10];
        new SecureRandom().nextBytes(buffer);
        Base32 base32 = new Base32();
        return base32.encodeToString(buffer);
    }

    private static String obterPaisDoIP() {
        try {
            URL url = new URL("https://ipinfo.io/country");
            Scanner sc = new Scanner(url.openStream());
            return sc.hasNext() ? sc.next().trim() : "Desconhecido";
        } catch (Exception e) {
            return "Erro ao obter local";
        }
    }

    private static boolean validarTotp(String secretBase32, String codigoDigitado) {
        long tempoAtual = System.currentTimeMillis() / 1000 / 30;
        for (int i = -1; i <= 1; i++) {
            String esperado = gerarTotpComTempo(secretBase32, tempoAtual + i);
            if (esperado.equals(codigoDigitado)) {
                return true;
            }
        }
        return false;
    }

    private static String gerarTotpComTempo(String secretBase32, long timeIndex) {
        try {
            Base32 base32 = new Base32();
            byte[] key = base32.decode(secretBase32);
            byte[] data = ByteBuffer.allocate(8).putLong(timeIndex).array();

            Mac mac = Mac.getInstance("HmacSHA1");
            mac.init(new SecretKeySpec(key, "HmacSHA1"));
            byte[] hmac = mac.doFinal(data);

            int offset = hmac[hmac.length - 1] & 0xf;
            int binary = ((hmac[offset] & 0x7f) << 24) |
                    ((hmac[offset + 1] & 0xff) << 16) |
                    ((hmac[offset + 2] & 0xff) << 8) |
                    (hmac[offset + 3] & 0xff);

            int otp = binary % 1000000;
            return String.format("%06d", otp);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao gerar TOTP com tempo", e);
        }
    }

    private static SecretKey derivarChave(String codigoTotp) {
        try {
            byte[] salt = "staticSaltParaDemo".getBytes(StandardCharsets.UTF_8);
            PBEKeySpec spec = new PBEKeySpec(codigoTotp.toCharArray(), salt, 10000, 128);
            SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
            byte[] chaveBytes = skf.generateSecret(spec).getEncoded();
            return new SecretKeySpec(chaveBytes, "AES");
        } catch (Exception e) {
            throw new RuntimeException("Erro ao derivar chave simétrica", e);
        }
    }

    private static byte[] cifrarMensagem(String mensagem, SecretKey chave, byte[] iv) {
        try {
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            GCMParameterSpec spec = new GCMParameterSpec(128, iv);
            cipher.init(Cipher.ENCRYPT_MODE, chave, spec);
            return cipher.doFinal(mensagem.getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            throw new RuntimeException("Erro ao cifrar mensagem", e);
        }
    }
}
