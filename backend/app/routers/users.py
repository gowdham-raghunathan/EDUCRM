from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, get_password_hash
from app.models import CRMUser, CRMTeam, CRMTeamMember
from app.schemas import UserCreate, UserRead, UserUpdate, TeamCreate, TeamRead, TeamUpdate, TeamMemberAdd

router = APIRouter(prefix='/api/users', tags=['User Management'])


# ─── Users ─────────────────────────────────────────────────────────────────────

@router.get('/', response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMUser).filter(CRMUser.deleted == False).order_by(CRMUser.created_at.desc()).all()


@router.get('/{user_id}', response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = db.query(CRMUser).filter(CRMUser.id == user_id, CRMUser.deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/', response_model=UserRead)
def create_user(data: UserCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if db.query(CRMUser).filter(CRMUser.username == data.username).first():
        raise HTTPException(status_code=400, detail='Username already exists')
    if data.email and db.query(CRMUser).filter(CRMUser.email == data.email).first():
        raise HTTPException(status_code=400, detail='Email already exists')

    user = CRMUser(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        role=data.role or 'counselor',
        mobile=data.mobile,
        department=data.department,
        employee_id=data.employee_id,
        password_hash=get_password_hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put('/{user_id}', response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = db.query(CRMUser).filter(CRMUser.id == user_id, CRMUser.deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    user = db.query(CRMUser).filter(CRMUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user.deleted = True
    db.commit()
    return {'message': 'User deleted'}


# ─── Teams ─────────────────────────────────────────────────────────────────────

@router.get('/teams/all', response_model=list[TeamRead])
def list_teams(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(CRMTeam).filter(CRMTeam.deleted == False).order_by(CRMTeam.created_at.desc()).all()


@router.post('/teams', response_model=TeamRead)
def create_team(data: TeamCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    team = CRMTeam(**data.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.put('/teams/{team_id}', response_model=TeamRead)
def update_team(team_id: int, data: TeamUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    team = db.query(CRMTeam).filter(CRMTeam.id == team_id, CRMTeam.deleted == False).first()
    if not team:
        raise HTTPException(status_code=404, detail='Team not found')
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(team, field, value)
    db.commit()
    db.refresh(team)
    return team


@router.post('/teams/{team_id}/members')
def add_team_member(team_id: int, data: TeamMemberAdd, db: Session = Depends(get_db), _=Depends(get_current_user)):
    existing = db.query(CRMTeamMember).filter(CRMTeamMember.team_id == team_id, CRMTeamMember.user_id == data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail='User already in team')
    member = CRMTeamMember(team_id=team_id, user_id=data.user_id)
    db.add(member)
    db.commit()
    return {'message': 'Member added', 'team_id': team_id, 'user_id': data.user_id}


@router.delete('/teams/{team_id}/members/{user_id}')
def remove_team_member(team_id: int, user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    member = db.query(CRMTeamMember).filter(CRMTeamMember.team_id == team_id, CRMTeamMember.user_id == user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail='Member not found')
    db.delete(member)
    db.commit()
    return {'message': 'Member removed'}


@router.delete('/teams/{team_id}')
def delete_team(team_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    team = db.query(CRMTeam).filter(CRMTeam.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail='Team not found')
    team.deleted = True
    db.commit()
    return {'message': 'Team deleted'}
