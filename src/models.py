from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

db = SQLAlchemy()

class TipoMedia(PyEnum):
    IMAGEN = "imagen"
    VIDEO = "video"

class User(db.Model):
    __tablename__ = 'usuario'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_de_usuario: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(10), nullable=False)
    apellido: Mapped[str] = mapped_column(String(15), nullable=False)
    correo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    comentarios: Mapped[list['Comentario']] = relationship(back_populates='autor')
    publicaciones: Mapped[list['Publicacion']] = relationship(back_populates='usuario')


class Comentario(db.Model):
    __tablename__ = 'comentario'
    id: Mapped[int] = mapped_column(primary_key=True)
    texto_comentario: Mapped[str] = mapped_column(String(200), nullable=False)
    autor_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    
    autor: Mapped['User'] = relationship(back_populates='comentarios')


class Publicacion(db.Model):
    __tablename__ = 'publicacion'
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    
    usuario: Mapped['User'] = relationship(back_populates='publicaciones')
    media: Mapped[list['Media']] = relationship(back_populates='publicacion')


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoMedia] = mapped_column(Enum(TipoMedia), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    publicacion_id: Mapped[int] = mapped_column(ForeignKey('publicacion.id'))
    
    publicacion: Mapped['Publicacion'] = relationship(back_populates='media')


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
