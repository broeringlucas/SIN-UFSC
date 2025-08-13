package org.lucas.broering;
import java.io.Serializable;

public class User implements Serializable {
    private String nome;
    private String celular;
    private String pais;
    private String senhaHash;
    private String salt;
    private String totpSecret; // Campo adicionado

    public User(String nome, String celular, String pais, String senhaHash, String salt, String totpSecret) {
        this.nome = nome;
        this.celular = celular;
        this.pais = pais;
        this.senhaHash = senhaHash;
        this.salt = salt;
        this.totpSecret = totpSecret;
    }

    // Getters
    public String getNome() { return nome; }
    public String getCelular() { return celular; }
    public String getPais() { return pais; }
    public String getSenhaHash() { return senhaHash; }
    public String getSalt() { return salt; }
    public String getTotpSecret() { return totpSecret; } // Getter adicionado
}