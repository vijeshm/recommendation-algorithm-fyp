#ifndef USERPROFILE_H
#define USERPROFILE_H

#include <QWidget>
#include <QProcess>

namespace Ui {
class userprofile;
}

class userprofile : public QWidget
{
    Q_OBJECT
    
public:
    QProcess *proc;
    QProcess *showprocess;
    QProcess *changeattrib;
    QString path;
    QProcess *attri;
    explicit userprofile(QWidget *parent = 0);
    ~userprofile();
    
private:
    Ui::userprofile *ui;


public slots:
    void movenext();
    void moveback();
    void generateuserprofile();
    void completed();
    void showclick();
    void showcompleted();
    void showimage();
    void attribshow();
    void attribchange();
    void imgzoom();

signals:
    void moverecucedimension();
    void movebacktoupload();
};

#endif // USERPROFILE_H
