package org.lucas.broering;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.*;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

public class Server {
    private static final String ARQUIVO_JSON = "usuarios.json";
    private List<User> usuarios;
    private Gson gson;

    public Server() {
        gson = new Gson();
        usuarios = carregarUsuarios();
    }

    private List<User> carregarUsuarios() {
        try (Reader reader = new FileReader(ARQUIVO_JSON)) {
            Type listType = new TypeToken<List<User>>() {}.getType();
            return gson.fromJson(reader, listType);
        } catch (IOException e) {
            return new ArrayList<>();
        }
    }

    private void salvarUsuarios() {
        try (Writer writer = new FileWriter(ARQUIVO_JSON)) {
            gson.toJson(usuarios, writer);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean cadastrarUsuario(User novoUsuario) {
        for (User u : usuarios) {
            if (u.getNome().equals(novoUsuario.getNome())) {
                return false;
            }
        }
        usuarios.add(novoUsuario);
        salvarUsuarios();
        return true;
    }

    public User buscarUsuario(String nome) {
        for (User u : usuarios) {
            if (u.getNome().equals(nome)) {
                return u;
            }
        }
        return null;
    }

    public String decifrarMensagem(byte[] mensagemCifrada, byte[] iv, SecretKey chave) throws Exception {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec spec = new GCMParameterSpec(128, iv);
        cipher.init(Cipher.DECRYPT_MODE, chave, spec);
        byte[] mensagem = cipher.doFinal(mensagemCifrada);
        return new String(mensagem);
    }
}