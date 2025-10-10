# 🔗 Cómo se Conecta el Frontend con el Backend

## 📊 Arquitectura de Conexión

```
┌──────────────────────────────────────────────────────────────┐
│                    Docker Network                            │
│                                                              │
│  ┌───────────────┐         HTTP         ┌──────────────┐   │
│  │   FRONTEND    │  ──────────────────> │   BACKEND    │   │
│  │   Angular     │                      │   FastAPI    │   │
│  │   :4200       │  <──────────────────│   :8000      │   │
│  └───────────────┘      JSON Response   └──────────────┘   │
│                                               │             │
│                                               ▼             │
│                                         ┌──────────┐        │
│                                         │  MYSQL   │        │
│                                         │  :3306   │        │
│                                         └──────────┘        │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔧 Servicios HTTP Configurados

Todos los servicios Angular se conectan al backend Python a través de HTTP:

### 1. **AuthService** (`services/auth.ts`)
```typescript
private apiUrl = 'http://localhost:8000/api/v1';

login(data):
  → POST http://localhost:8000/api/v1/userses/login

register(data):
  → POST http://localhost:8000/api/v1/userses
```

### 2. **VehiclesService** (`services/vehicles.ts`)
```typescript
getVehicles():
  → GET http://localhost:8000/api/v1/vehicles/

createVehicle(data):
  → POST http://localhost:8000/api/v1/vehicles/
```

### 3. **DriversService** (`services/drivers.ts`)
```typescript
getDrivers():
  → GET http://localhost:8000/api/v1/drivers/

createDriver(data):
  → POST http://localhost:8000/api/v1/drivers/
```

### 4. **ClientsService** (`services/clients.ts`)
```typescript
getClients():
  → GET http://localhost:8000/api/v1/clients/

createClient(data):
  → POST http://localhost:8000/api/v1/clients/
```

### 5. **AddressesService** (`services/addresses.ts`)
```typescript
getAddresses():
  → GET http://localhost:8000/api/v1/addresses/

createAddress(data):
  → POST http://localhost:8000/api/v1/addresses/
```

### 6. **GeocodingService** (`services/geocoding.service.ts`)
```typescript
geocodeAddress(address):
  → POST http://localhost:8000/api/v1/geocoding/
```

---

## 🌐 Detección Automática de Entorno

Los servicios detectan automáticamente si están en:

```typescript
constructor(@Inject(PLATFORM_ID) private platformId: Object) {
  this.apiUrl = isPlatformBrowser(this.platformId) 
    ? 'http://localhost:8000/api/v1'  // Navegador → localhost
    : 'http://app:8000/api/v1';       // Docker SSR → nombre del servicio
}
```

**¿Por qué?**
- **En el navegador:** Usa `localhost:8000` porque el usuario accede desde fuera de Docker
- **En Docker SSR:** Usa `app:8000` porque está dentro de la red Docker

---

## 📡 Ejemplo Completo: Flujo de Registro

### **Paso 1: Usuario completa formulario (Frontend)**
```html
<!-- register.html -->
<form (ngSubmit)="onSubmit()">
  <input [(ngModel)]="username" />
  <input [(ngModel)]="password" />
  <button>Crear cuenta</button>
</form>
```

### **Paso 2: Componente llama al servicio (Angular)**
```typescript
// register.ts
onSubmit() {
  this.auth.register({ 
    username: this.username, 
    password: this.password 
  }).subscribe({
    next: (response) => { /* Éxito */ },
    error: (err) => { /* Error */ }
  });
}
```

### **Paso 3: Servicio hace petición HTTP (Angular → Python)**
```typescript
// auth.ts
register(data): Observable<any> {
  return this.http.post('http://localhost:8000/api/v1/userses', data);
  //                     ↑ Petición HTTP al backend
}
```

### **Paso 4: Backend recibe la petición (FastAPI)**
```python
# userses.py
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user)
```

### **Paso 5: Servicio procesa (Python)**
```python
# users_service.py
def create_user(self, db: Session, user: UserCreate):
    return self.repository.create_user(db, user)
```

### **Paso 6: Repository guarda en DB (SQLAlchemy → MySQL)**
```python
# users_repository.py
def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    return db_user  # ← Devuelve al backend
```

### **Paso 7: Backend devuelve JSON (Python → Angular)**
```json
{
  "username": "admin",
  "id": 1,
  "is_active": true
}
```

### **Paso 8: Frontend muestra resultado (Angular)**
```typescript
next: (response) => {
  alert('Usuario creado exitosamente!');
  this.router.navigate(['/login']);
}
```

---

## ✅ CORS Configurado

El backend tiene CORS habilitado para permitir peticiones desde el frontend:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔍 Verificar la Conexión

### Desde el navegador:
1. Abre http://localhost:4200
2. Presiona F12 (Consola del desarrollador)
3. Ve a la pestaña "Network"
4. Registra un usuario
5. Verás las peticiones HTTP a `localhost:8000`

---

## 🎯 Endpoints Conectados

| Acción Frontend | Método HTTP | URL Backend |
|----------------|-------------|-------------|
| Registro | POST | `/api/v1/userses` |
| Login | POST | `/api/v1/userses/login` |
| Listar Vehículos | GET | `/api/v1/vehicles/` |
| Crear Vehículo | POST | `/api/v1/vehicles/` |
| Listar Conductores | GET | `/api/v1/drivers/` |
| Crear Conductor | POST | `/api/v1/drivers/` |
| Listar Clientes | GET | `/api/v1/clients/` |
| Crear Cliente | POST | `/api/v1/clients/` |
| Listar Direcciones | GET | `/api/v1/addresses/` |
| Crear Dirección | POST | `/api/v1/addresses/` |
| Geocodificar | POST | `/api/v1/geocoding/` |

---

## 🚀 La Conexión es Automática

**No necesitas hacer nada manual** para conectar:
- ✅ Los servicios ya están configurados
- ✅ Las URLs ya apuntan al backend
- ✅ CORS ya está habilitado
- ✅ Docker network permite la comunicación

**Todo funciona automáticamente** cuando haces `docker-compose up` 🎉

