from py_modules.utils.di import inject, bean

@bean
class Repository:
    def get_data(self):
        return "Data from Repository"

@inject
class Service:
    repo: Repository  # Campo de instancia anotado

    def perform_action(self):
        data = self.repo.get_data()
        return f"Action performed with: {data}"

# Ejemplo de uso
if __name__ == "__main__":
    service = Service()  # La dependencia se inyecta automáticamente
    result = service.perform_action()
    print(result)  # Imprime: Action performed with: Data from Repository
