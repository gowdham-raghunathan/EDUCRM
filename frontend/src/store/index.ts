import { configureStore, createSlice } from '@reduxjs/toolkit'

interface AppState {
  activeModule: string
}

const initialState: AppState = {
  activeModule: 'Dashboard',
}

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {
    setActiveModule: (state, action) => {
      state.activeModule = action.payload
    },
  },
})

export const { setActiveModule } = appSlice.actions

export const store = configureStore({
  reducer: {
    app: appSlice.reducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
